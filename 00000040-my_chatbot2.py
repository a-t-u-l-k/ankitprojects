import random

def chatbot_response(user_input):
    # Define categories with responses
    responses = {
        "greetings": [
            "Hello! How can I assist you today?", "Hi there! What can I do for you?", "Hey! How can I help you?",
            "Greetings! What’s on your mind?", "Hello! How are you today?", "Hi! What’s up?", 
            "Hey there! What can I help with?", "Hello! How can I make your day better?",
            "Hi! How can I assist you?", "Greetings! What do you need help with?",
            "Hello! What brings you here today?", "Hi there! How can I assist?", 
            "Hey! What’s on your mind?", "Greetings! How can I be of service?", 
            "Hello! What can I do for you today?", "Hi! How can I help you out?",
            "Hey there! What’s up?", "Greetings! How can I support you?", 
            "Hello! What’s new with you?", "Hi! What can I assist with?"
        ],
        "farewells": [
            "Goodbye! Take care!", "See you later!", "Bye! Have a great day!", 
            "Farewell! Wishing you all the best!", "Take care! See you soon!",
            "Goodbye! Have a good one!", "See you next time!", "Bye! All the best!",
            "Farewell! Take care of yourself!", "Goodbye! Stay safe!", "See you later!",
            "Bye! Have a great time!", "Farewell! Until next time!", "Take care!",
            "Goodbye! Wish you well!", "See you around!", "Bye! Have a wonderful day!",
            "Farewell! Enjoy your day!", "Goodbye! Take care and stay well!",
            "See you later! All the best!", "Bye! Hope to see you soon!"
        ],
        "emotions": {
            "happy": [
                "I’m glad to hear you’re feeling happy! What’s making you feel this way?",
                "Your happiness is wonderful! What’s bringing you joy?", "It’s great to see you so happy! What’s the cause?",
                "I’m thrilled to hear about what’s making you feel this way. Share with me!",
                "Your positive mood is contagious! What’s making you so happy?", "I’m excited to hear what’s bringing you happiness.",
                "Your joy is amazing! What’s the reason?", "It’s wonderful to see you smiling. What’s the cause of your happiness?",
                "I’m happy to hear you’re feeling this way. What’s behind your happiness?", "What’s making you so joyful? Let’s talk about it.",
                "Your happiness is fantastic! What’s the boost?", "It’s great to see you so upbeat. What’s the reason for your joy?",
                "I’m thrilled to see you feeling this way. What’s the cause?", "Your positive attitude is inspiring! What’s making you happy?",
                "I’m glad to hear you’re feeling joyful. What’s the reason?", "It’s wonderful to see you smiling. What’s behind your happiness?",
                "Your joy is infectious! What’s the reason for your happiness?", "I’m excited to hear about what’s making you feel this way.",
                "Your happiness is amazing! What’s giving you this feeling?", "It’s great to see you so happy. What’s the cause?"
            ],
            "apathetic": [
                "It seems like you’re feeling apathetic. Is there something specific that’s causing this feeling?",
                "Apathy can be tough. Let’s talk about what’s on your mind.", "I understand you’re feeling apathetic. How can I help?",
                "It’s okay to feel apathetic sometimes. What’s going on?", "Apathy can be a sign of something deeper. Want to talk about it?",
                "I hear you’re feeling apathetic. What might be causing this feeling?", "Feeling apathetic can be challenging. Let’s explore it together.",
                "If you’re feeling apathetic, I’m here to listen. What’s going on?", "Apathy can be a response to many things. Let’s discuss it.",
                "It’s normal to feel apathetic at times. What’s happening?", "Apathy can be a sign of many things. Let’s talk about it.",
                "I’m here to support you through this apathetic feeling. What’s up?", "Feeling apathetic can be tough. Let’s address it.",
                "Let’s work through this apathy together. What’s causing it?", "Apathy is valid. How can I assist you?",
                "I understand you’re feeling apathetic. Let’s explore what’s behind it.", "Feeling apathetic can be a response to many factors.",
                "I’m here to support you. What’s behind your apathy?", "Let’s talk about this feeling of apathy you’re experiencing.",
                "It’s okay to feel apathetic. Let’s work on understanding it.", "Apathy can be challenging. What’s going on?"
            ],
            # Add responses for other emotions similarly
        }
    }
    
    # Check for basic responses
    if any(word in user_input.lower() for word in ["hello", "hi", "hey", "greeting"]):
        return random.choice(responses["greetings"])
    if any(word in user_input.lower() for word in ["bye", "goodbye", "see you", "later"]):
        return random.choice(responses["farewells"])
    
    # Check for emotional responses
    for emotion, response_list in responses["emotions"].items():
        if emotion in user_input.lower():
            return random.choice(response_list)
    
    # Debugging output
    print(f"User input: {user_input}")
    print("Responses checked:", list(responses["emotions"].keys()))
    
    return "I’m not sure how to respond to that. Can you tell me more?"

def main():
    print("Hello! I'm your chatbot. Type 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye! Take care!")
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
