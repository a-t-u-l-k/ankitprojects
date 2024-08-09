import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def generate_response(user_input):
    # Encode the input and generate a response
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def chatbot_response(user_input):
    # Define categories with responses (as before)
    responses = {
        "greetings": [
            "Hi there! How can I assist you today?",
            "Hello! What can I do for you?",
            # ... (other greetings)
        ],
        "farewells": [
            "Goodbye! Take care!",
            "See you later! Have a good day!",
            # ... (other farewells)
        ],
        # ... (other categories and responses)
    }

    user_input = user_input.lower()

    # Check for basic responses
    if any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
        return random.choice(responses["greetings"])
    if any(word in user_input for word in ["bye", "goodbye", "see you", "later"]):
        return random.choice(responses["farewells"])

    # Fallback to GPT-2 response if no predefined response matches
    return generate_response(user_input)

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