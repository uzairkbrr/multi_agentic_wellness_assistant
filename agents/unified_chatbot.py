import base64
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from together import Together
from utils.config import TOGETHER_API_KEY
from agents.vision import analyze_meal_image
from agents.diet import analyze_meal_text, extract_meal_name
from agents.exercise import get_exercise_plan
from agents.mental_health import get_mental_health_response
from backend.crud import (
    insert_meal_log, list_meal_logs, insert_workout_log, list_workout_logs,
    insert_memory, list_memories, log_activity, get_user_by_id
)
from datetime import datetime


TEXT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
VISION_MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"


def _client() -> Together:
    if not TOGETHER_API_KEY:
        raise ValueError(
            "❌ TOGETHER_API_KEY is missing. "
            "For localhost: Create a .env file with TOGETHER_API_KEY=your_key_here\n"
            "For deployment: Set TOGETHER_API_KEY in Streamlit secrets"
        )
    return Together(api_key=TOGETHER_API_KEY)


def is_wellness_related(user_message: str) -> bool:
    """
    Check if the user message is wellness-related (diet, exercise, mental health, fitness, nutrition, etc.)
    """
    wellness_keywords = [
        # Diet and nutrition
        'diet', 'nutrition', 'food', 'meal', 'calorie', 'protein', 'carb', 'fat', 'vitamin',
        'healthy', 'eating', 'weight', 'lose', 'gain', 'maintain', 'bmi', 'portion',
        'breakfast', 'lunch', 'dinner', 'snack', 'water', 'hydrate', 'supplement',
        
        # Exercise and fitness
        'exercise', 'workout', 'fitness', 'training', 'gym', 'cardio', 'strength',
        'muscle', 'running', 'walking', 'cycling', 'swimming', 'yoga', 'pilates',
        'stretching', 'flexibility', 'endurance', 'stamina', 'energy', 'active',
        
        # Mental health
        'stress', 'anxiety', 'depression', 'mood', 'mental', 'emotional', 'wellbeing',
        'sleep', 'rest', 'relax', 'meditation', 'mindfulness', 'therapy', 'counseling',
        'happiness', 'joy', 'sadness', 'anger', 'fear', 'worry', 'confidence',
        
        # General wellness
        'health', 'wellness', 'lifestyle', 'habit', 'routine', 'goal', 'progress',
        'track', 'monitor', 'improve', 'better', 'healthy', 'unhealthy', 'balance',
        'recovery', 'rest', 'sleep', 'energy', 'vitality', 'strength', 'weakness',
        
        # Body and physical
        'body', 'physical', 'pain', 'ache', 'injury', 'recovery', 'healing',
        'symptom', 'condition', 'medical', 'doctor', 'healthcare', 'treatment',
        
        # Personal wellness
        'my health', 'my diet', 'my exercise', 'my fitness', 'my mental health',
        'help me', 'advice', 'recommendation', 'suggestion', 'plan', 'program'
    ]
    
    message_lower = user_message.lower()
    
    # Check for wellness keywords
    for keyword in wellness_keywords:
        if keyword in message_lower:
            return True
    
    # Check for wellness-related patterns
    wellness_patterns = [
        r'\b(how|what|when|where|why)\s+(should|can|do|is|are)\s+(i|you|we)\s+(eat|exercise|workout|train|sleep|rest|relax|meditate|improve|get|become|feel|stay|maintain|lose|gain)\b',
        r'\b(i|i\'m|am)\s+(feeling|feeling|tired|stressed|anxious|depressed|happy|sad|angry|worried|confident|weak|strong|healthy|unhealthy)\b',
        r'\b(my|i need|i want|help me|advice|recommendation|suggestion)\s+(diet|exercise|workout|fitness|health|mental|nutrition|weight|muscle|strength|energy|sleep|stress)\b',
        r'\b(analyze|check|evaluate|assess|review)\s+(my|this|the)\s+(food|meal|nutrition|diet|exercise|workout|fitness|health|progress)\b',
        r'\b(generate|create|make|give|provide)\s+(a|an)\s+(diet|exercise|workout|fitness|health|mental|nutrition|plan|program|routine)\b'
    ]
    
    for pattern in wellness_patterns:
        if re.search(pattern, message_lower):
            return True
    
    return False


def get_user_context(user_id: int) -> Dict[str, Any]:
    """
    Get user's wellness context from database
    """
    try:
        # Get user profile
        user = get_user_by_id(user_id)
        
        # Get recent activity
        recent_meals = list_meal_logs(user_id, limit=5)
        recent_workouts = list_workout_logs(user_id, limit=5)
        recent_memories = list_memories(user_id, limit=3)
        
        context = {
            "user_profile": user or {},
            "recent_meals": recent_meals,
            "recent_workouts": recent_workouts,
            "recent_memories": recent_memories,
            "total_meals": len(list_meal_logs(user_id, limit=1000)),
            "total_workouts": len(list_workout_logs(user_id, limit=1000)),
            "total_memories": len(list_memories(user_id, limit=1000))
        }
        
        return context
    except Exception as e:
        return {"error": str(e)}


def generate_unified_response(
    user_message: str, 
    user_id: int, 
    chat_history: List[Dict[str, str]] = None,
    image_path: str = None
) -> Dict[str, Any]:
    """
    Main function to handle user messages and generate unified responses.
    Only responds to wellness-related questions using database information.
    """
    if chat_history is None:
        chat_history = []
    
    # Check if message is wellness-related
    if not is_wellness_related(user_message):
        return {
            "response": "I'm a wellness assistant focused on helping you with health, nutrition, exercise, and mental wellbeing. I can help you with:\n\n• **Diet & Nutrition**: Food analysis, meal planning, nutrition advice\n• **Exercise & Fitness**: Workout plans, fitness guidance, training advice\n• **Mental Health**: Stress management, emotional support, wellness guidance\n• **Progress Tracking**: Analyze your wellness data and provide insights\n\nPlease ask me about any of these wellness topics!",
            "type": "wellness_only"
        }
    
    # Get user context from database
    user_context = get_user_context(user_id)
    
    try:
        # Handle image analysis (food photos)
        if image_path and any(word in user_message.lower() for word in ['analyze', 'check', 'what', 'food', 'meal', 'nutrition']):
            analysis = analyze_meal_image(image_path)
            if "error" in analysis:
                return {"response": f"❌ {analysis['error']}", "type": "error"}
            
            # Extract meal name and log to database
            meal_name = extract_meal_name(user_message) if user_message.strip() else "Analyzed Meal"
            meal_id = insert_meal_log(
                user_id=user_id,
                meal_name=meal_name,
                meal_description=user_message,
                calories_est="Analyzed from image",
                date=datetime.now().date().isoformat()
            )
            
            # Log activity
            log_activity(user_id, "meal_analyzed", {
                "meal_id": meal_id,
                "meal_name": meal_name,
                "analysis": analysis.get("raw", "")
            })
            
            return {
                "response": f"🍽️ **Food Analysis Complete!**\n\n{analysis.get('raw', 'Analysis completed')}\n\nI've logged this meal to your wellness tracker.",
                "type": "food_analysis",
                "meal_id": meal_id
            }
        
        # Handle text-based wellness questions
        client = _client()
        
        # Create context-aware prompt
        context_info = ""
        if user_context.get("user_profile"):
            profile = user_context["user_profile"]
            context_info += f"\n\n**Your Profile:** Age: {profile.get('age', 'Not set')}, Goal: {profile.get('fitness_goal', 'Not set')}, Activity: {profile.get('activity_level', 'Not set')}"
        
        if user_context.get("recent_meals"):
            recent_meals = user_context["recent_meals"][:3]
            meal_names = [m.get("meal_name", "Unknown") for m in recent_meals]
            context_info += f"\n**Recent Meals:** {', '.join(meal_names)}"
        
        if user_context.get("recent_workouts"):
            recent_workouts = user_context["recent_workouts"][:3]
            workout_names = [w.get("workout_name", "Unknown") for w in recent_workouts]
            context_info += f"\n**Recent Workouts:** {', '.join(workout_names)}"
        
        # Create system prompt
        system_prompt = f"""You are a wellness assistant that provides personalized health, nutrition, exercise, and mental health advice. 

Use the user's profile and recent activity to provide personalized recommendations.

**Important Guidelines:**
- Only provide wellness-related advice (diet, exercise, mental health, fitness, nutrition)
- Use the user's context to personalize your responses
- Be encouraging, practical, and evidence-based
- If the user asks about non-wellness topics, politely redirect them to wellness topics
- Always consider the user's goals, activity level, and recent progress

**User Context:**{context_info}

**User Question:** {user_message}

Provide a helpful, personalized wellness response:"""

        # Generate response
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=512,
        )
        
        content = response.choices[0].message.content
        if isinstance(content, list):
            content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
        
        # Log the interaction
        log_activity(user_id, "wellness_chat", {
            "user_message": user_message[:200],
            "response_type": "wellness_advice"
        })
        
        return {
            "response": content or "I'm here to help with your wellness journey!",
            "type": "wellness_advice"
        }
    
    except Exception as e:
        return {
            "response": f"❌ Sorry, I encountered an error: {str(e)}",
            "type": "error"
        }


def process_voice_input(audio_data: bytes) -> str:
    """
    Process voice input and convert to text.
    This is a placeholder - you'll need to integrate with a speech-to-text service.
    """
    # For now, return a placeholder message
    # In a real implementation, you would:
    # 1. Send audio_data to a speech-to-text service (Google Speech-to-Text, Whisper, etc.)
    # 2. Return the transcribed text
    
    return "Voice input received. Please type your message for now."
