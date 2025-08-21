# 🤖 Wellness Assistant

A unified AI-powered wellness assistant with a ChatGPT-style interface that helps you with nutrition, exercise, and mental health through natural language conversation.

## ✨ Features

### 🍽️ **Nutrition & Diet**
- **Food Image Analysis**: Upload photos of your meals for instant nutritional analysis
- **Meal Suggestions**: Get personalized diet advice and meal recommendations
- **Calorie Tracking**: Automatic logging of analyzed meals to your wellness tracker

### 💪 **Exercise & Fitness**
- **Workout Plans**: Get personalized exercise routines and fitness advice
- **Exercise Guidance**: Ask about specific exercises, techniques, and training methods
- **Progress Tracking**: Monitor your fitness journey with detailed reports

### 🧠 **Mental Health**
- **Emotional Support**: Share your feelings and get empathetic responses
- **Stress Management**: Get advice on managing stress and anxiety
- **Conversation Memory**: Your mental health conversations are remembered for continuity

### 📊 **Reports & Analytics**
- **Wellness Reports**: Generate comprehensive reports of your health journey
- **Activity Tracking**: Monitor meals, workouts, and mental health conversations
- **Progress Insights**: Get personalized recommendations based on your data

### 🎤 **Voice Input**
- **Speech Recognition**: Speak to your assistant instead of typing
- **Natural Conversation**: Have fluid conversations about your wellness goals
- **Browser-Based**: Works in modern browsers with speech recognition support

## 🚀 Setup

### For Localhost Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```
   TOGETHER_API_KEY=your_actual_together_api_key_here
   ```
   
   Get your API key from: https://api.together.xyz/settings/api-keys

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### For Deployment (Streamlit Cloud)

1. **Set Streamlit secrets:**
   In your Streamlit Cloud dashboard, go to Settings → Secrets and add:
   ```toml
   TOGETHER_API_KEY = "your_actual_together_api_key_here"
   ```

2. **Deploy:**
   Connect your repository to Streamlit Cloud and deploy.

## 💬 How to Use

### Getting Started
1. **Login/Register**: Create an account or log in to your existing account
2. **Start Chatting**: Navigate to the chat interface and start asking questions
3. **Upload Images**: Use the file uploader to analyze food photos
4. **Voice Input**: Click the microphone button to speak your questions

### Example Conversations
- **"What should I eat today?"** - Get personalized meal suggestions
- **"Analyze this food"** (with image) - Get nutritional breakdown
- **"I'm feeling stressed"** - Receive mental health support
- **"Give me an exercise plan"** - Get personalized workout recommendations
- **"Generate my wellness report"** - See your progress summary

## 🏗️ Application Structure

The application consists of **4 main pages**:

1. **Landing Page** (`pages/landing_page.py`) - Welcome and introduction
2. **Login/Signup** (integrated in `app.py`) - User authentication
3. **Unified Chatbot** (`pages/unified_chatbot.py`) - Main AI assistant interface
4. **Profile** (`pages/profile.py`) - User profile management

## 🛠️ Technical Details

- **AI Models**: Powered by Together AI's Llama models
- **Database**: SQLite with automatic meal/workout/memory logging
- **Voice Input**: HTML5 Speech Recognition API
- **Image Analysis**: Vision model for food nutrition analysis
- **Memory**: Persistent conversation history and wellness tracking
- **UI**: ChatGPT-style clean, minimal interface

## 📝 Notes

- Uses SQLite at `data/wellness.db` created on first run
- All conversations and wellness data are stored locally
- Voice input requires browser microphone permissions
- The app automatically detects whether it's running locally (uses .env) or deployed (uses Streamlit secrets)

## 🔒 Privacy

- All data is stored locally in your SQLite database
- No personal information is shared with third parties
- Voice input is processed locally in your browser
- API calls only send necessary data for AI processing

