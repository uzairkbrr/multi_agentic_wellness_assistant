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
    insert_memory, list_memories, log_activity
)
from datetime import datetime, timezone


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


def classify_user_intent(user_message: str) -> Dict[str, Any]:
    """
    Classify user intent and extract relevant information from the message.
    Returns a dict with intent type and extracted parameters.
    """
    client = _client()
    
    system_prompt = """You are an intent classifier for a wellness assistant. Analyze the user's message and classify their intent into one of these categories:

1. DIET_ANALYSIS - User wants to analyze food/nutrition (e.g., "analyze this food", "what's in this meal", "check nutrition")
2. DIET_SUGGESTION - User wants diet advice (e.g., "what should I eat", "meal suggestions", "diet plan")
3. EXERCISE_PLAN - User wants exercise advice (e.g., "workout plan", "exercise routine", "fitness advice")
4. MENTAL_HEALTH - User wants mental health support (e.g., "I'm stressed", "feeling anxious", "mental health advice")
5. REPORT_GENERATION - User wants a report (e.g., "generate report", "show my progress", "dashboard")
6. GENERAL_CHAT - General conversation or unclear intent

Also extract any relevant parameters like:
- food_image: if user mentions analyzing an image
- meal_description: if user describes a meal
- exercise_type: if user mentions specific exercise
- mood: if user mentions their emotional state

Respond with JSON only:
{
    "intent": "INTENT_TYPE",
    "confidence": 0.0-1.0,
    "parameters": {
        "food_image": boolean,
        "meal_description": string or null,
        "exercise_type": string or null,
        "mood": string or null
    }
}"""

    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=256,
        )
        
        content = response.choices[0].message.content
        if isinstance(content, list):
            content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Fallback classification
            message_lower = user_message.lower()
            if any(word in message_lower for word in ["food", "meal", "nutrition", "calories", "diet"]):
                return {"intent": "DIET_SUGGESTION", "confidence": 0.7, "parameters": {}}
            elif any(word in message_lower for word in ["exercise", "workout", "fitness", "training"]):
                return {"intent": "EXERCISE_PLAN", "confidence": 0.7, "parameters": {}}
            elif any(word in message_lower for word in ["stress", "anxiety", "mood", "mental", "feel"]):
                return {"intent": "MENTAL_HEALTH", "confidence": 0.7, "parameters": {}}
            elif any(word in message_lower for word in ["report", "progress", "dashboard", "summary"]):
                return {"intent": "REPORT_GENERATION", "confidence": 0.7, "parameters": {}}
            else:
                return {"intent": "GENERAL_CHAT", "confidence": 0.5, "parameters": {}}
                
    except Exception as e:
        # Fallback classification
        message_lower = user_message.lower()
        if any(word in message_lower for word in ["food", "meal", "nutrition", "calories", "diet"]):
            return {"intent": "DIET_SUGGESTION", "confidence": 0.6, "parameters": {}}
        elif any(word in message_lower for word in ["exercise", "workout", "fitness", "training"]):
            return {"intent": "EXERCISE_PLAN", "confidence": 0.6, "parameters": {}}
        elif any(word in message_lower for word in ["stress", "anxiety", "mood", "mental", "feel"]):
            return {"intent": "MENTAL_HEALTH", "confidence": 0.6, "parameters": {}}
        elif any(word in message_lower for word in ["report", "progress", "dashboard", "summary"]):
            return {"intent": "REPORT_GENERATION", "confidence": 0.6, "parameters": {}}
        else:
            return {"intent": "GENERAL_CHAT", "confidence": 0.5, "parameters": {}}


def generate_unified_response(
    user_message: str, 
    user_id: int, 
    chat_history: List[Dict[str, str]] = None,
    image_path: str = None
) -> Dict[str, Any]:
    """
    Main function to handle user messages and generate unified responses.
    Returns a dict with response text and any additional data.
    """
    if chat_history is None:
        chat_history = []
    
    # Classify user intent
    intent_data = classify_user_intent(user_message)
    intent = intent_data["intent"]
    parameters = intent_data.get("parameters", {})
    
    try:
        if intent == "DIET_ANALYSIS":
            if image_path:
                # Analyze food image
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
                    date=datetime.now(timezone.utc).date().isoformat()
                )
                
                # Log activity
                log_activity(user_id, "meal_analyzed", {
                    "meal_id": meal_id,
                    "meal_name": meal_name,
                    "analysis": analysis.get("raw", "")
                })
                
                return {
                    "response": f"🍽️ **Meal Analysis Complete!**\n\n{analysis.get('raw', 'Analysis completed')}\n\nI've logged this meal to your tracker.",
                    "type": "diet_analysis",
                    "meal_id": meal_id
                }
            else:
                # Analyze text-based meal description
                analysis = analyze_meal_text(user_message)
                meal_name = extract_meal_name(user_message)
                meal_id = insert_meal_log(
                    user_id=user_id,
                    meal_name=meal_name,
                    meal_description=user_message,
                    calories_est="Analyzed from description",
                    date=datetime.now(timezone.utc).date().isoformat()
                )
                
                log_activity(user_id, "meal_analyzed", {
                    "meal_id": meal_id,
                    "meal_name": meal_name,
                    "analysis": analysis
                })
                
                return {
                    "response": f"🍽️ **Meal Analysis Complete!**\n\n{analysis}\n\nI've logged this meal to your tracker.",
                    "type": "diet_analysis",
                    "meal_id": meal_id
                }
        
        elif intent == "DIET_SUGGESTION":
            # Get diet suggestions
            messages = [
                {"role": "system", "content": "You are a helpful nutritionist providing personalized diet advice. Be encouraging and practical."},
                {"role": "user", "content": user_message}
            ]
            
            # Add context from recent meals if available
            recent_meals = list_meal_logs(user_id, limit=5)
            if recent_meals:
                meal_context = "Recent meals: " + ", ".join([m.get("meal_name", "Unknown") for m in recent_meals[:3]])
                messages[1]["content"] += f"\n\nContext: {meal_context}"
            
            suggestion = get_mental_health_response(messages)  # Reusing the same function structure
            
            return {
                "response": f"🥗 **Nutrition Advice**\n\n{suggestion}",
                "type": "diet_suggestion"
            }
        
        elif intent == "EXERCISE_PLAN":
            # Get exercise recommendations
            messages = [
                {"role": "system", "content": "You are a helpful fitness trainer providing personalized exercise advice. Be encouraging and practical."},
                {"role": "user", "content": user_message}
            ]
            
            # Add context from recent workouts if available
            recent_workouts = list_workout_logs(user_id, limit=5)
            if recent_workouts:
                workout_context = "Recent workouts: " + ", ".join([w.get("workout_name", "Unknown") for w in recent_workouts[:3]])
                messages[1]["content"] += f"\n\nContext: {workout_context}"
            
            plan = get_exercise_plan(messages)
            
            return {
                "response": f"💪 **Exercise Plan**\n\n{plan}",
                "type": "exercise_plan"
            }
        
        elif intent == "MENTAL_HEALTH":
            # Handle mental health conversation
            messages = [
                {"role": "system", "content": "You are a supportive mental health companion. Be empathetic, encouraging, and helpful."},
                {"role": "user", "content": user_message}
            ]
            
            # Add context from recent memories if available
            recent_memories = list_memories(user_id, limit=3)
            if recent_memories:
                memory_context = "Recent conversations: " + ", ".join([m.get("summary", "")[:50] + "..." for m in recent_memories])
                messages[1]["content"] += f"\n\nContext: {memory_context}"
            
            response = get_mental_health_response(messages)
            
            # Store memory of this conversation
            memory_id = insert_memory(
                user_id=user_id,
                summary=f"User: {user_message[:100]}... | Assistant: {response[:100]}...",
                tags="mental_health"
            )
            
            log_activity(user_id, "mental_health_chat", {
                "memory_id": memory_id,
                "user_message": user_message[:200]
            })
            
            return {
                "response": f"🧠 **Mental Health Support**\n\n{response}",
                "type": "mental_health",
                "memory_id": memory_id
            }
        
        elif intent == "REPORT_GENERATION":
            # Generate a wellness report
            meals = list_meal_logs(user_id, limit=50)
            workouts = list_workout_logs(user_id, limit=50)
            memories = list_memories(user_id, limit=10)
            
            # Calculate some basic stats
            total_meals = len(meals)
            total_workouts = len(workouts)
            recent_meals = len([m for m in meals if m.get("date") and str(m["date"]) >= str((datetime.now(timezone.utc).date().isoformat()))])
            recent_workouts = len([w for w in workouts if w.get("date") and str(w["date"]) >= str((datetime.now(timezone.utc).date().isoformat()))])
            
            report = f"""📊 **Your Wellness Report**

**Activity Summary:**
• Total meals logged: {total_meals}
• Total workouts logged: {total_workouts}
• Recent meals (today): {recent_meals}
• Recent workouts (today): {recent_workouts}

**Recent Activity:**
• Last meal: {meals[0].get('meal_name', 'None') if meals else 'None'}
• Last workout: {workouts[0].get('workout_name', 'None') if workouts else 'None'}
• Mental health conversations: {len(memories)}

**Recommendations:**
• Keep up the great work with your wellness tracking!
• Consider logging your next meal or workout
• Take time for mental health reflection

Would you like me to help you with anything specific today?"""
            
            return {
                "response": report,
                "type": "report",
                "stats": {
                    "total_meals": total_meals,
                    "total_workouts": total_workouts,
                    "recent_meals": recent_meals,
                    "recent_workouts": recent_workouts
                }
            }
        
        else:
            # General chat - be helpful and guide to specific features
            messages = [
                {"role": "system", "content": "You are a friendly wellness assistant. Help users with their health and fitness goals. If they ask general questions, guide them to specific features like meal tracking, exercise planning, or mental health support."},
                {"role": "user", "content": user_message}
            ]
            
            response = get_mental_health_response(messages)
            
            return {
                "response": f"👋 **Wellness Assistant**\n\n{response}",
                "type": "general_chat"
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
