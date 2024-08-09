from transformers import MarianMTModel, MarianTokenizer
import pandas as pd

# Initialize the model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-hi'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# List of 100 most common daily life sentences in English
english_sentences = [
    "Hello", "How are you?", "Good morning", "Good night", "Thank you", "You're welcome",
    "Please", "Excuse me", "I'm sorry", "What is your name?", "My name is...", 
    "Nice to meet you", "How much is this?", "Where is the restroom?", "I don't understand",
    "Can you help me?", "What time is it?", "I'm lost", "I need a doctor", "Call the police",
    "I love you", "Do you speak English?", "I speak a little Hindi", "What's your phone number?",
    "I'm hungry", "I'm thirsty", "I'm tired", "What is this?", "How do you say ... in Hindi?",
    "Can you repeat that?", "Where are you from?", "I'm from...", "I live in...", "Do you have...?",
    "Can I have...?", "How far is it?", "I would like...", "I'm looking for...", "Can I pay by card?",
    "Cash only", "Do you have a menu?", "I'm a vegetarian", "No, thank you", "Yes, please",
    "That's great", "Congratulations", "Good job", "I'm proud of you", "Take care", "Get well soon",
    "Happy birthday", "Merry Christmas", "Happy New Year", "Where can I buy...?", "I need water",
    "It's an emergency", "Can I use your phone?", "Where is the nearest ATM?", "I don't feel well",
    "What's the weather like?", "Can you give me directions?", "Can I borrow...?", "How long will it take?",
    "Is there a bus/train station nearby?", "I missed my bus/train", "I need a taxi", "Please write it down",
    "I'm learning Hindi", "What does ... mean?", "Can you speak slowly?", "I have a reservation",
    "Is breakfast included?", "I would like to check out", "Can I get a receipt?", "Is Wi-Fi available?",
    "The password is...", "I need to charge my phone", "Can I get a wake-up call?", "Is there a pharmacy nearby?",
    "Can I get a map?", "Is there a supermarket nearby?", "I need to go to the airport", "How much is the fare?",
    "Do you accept credit cards?", "I need an appointment", "Where is the hospital?", "Can you call a taxi for me?",
    "Where can I find a grocery store?", "Can you recommend a good restaurant?", "I need a room for two nights",
    "Is there a laundry service?", "Can I get an extra pillow?", "Is there a gym in the hotel?",
    "What are the tourist attractions?", "Where can I exchange money?", "Is there a parking lot?", "Can I rent a car?",
    "I lost my key", "Can you send someone to help?", "I'm checking in",
]

# Function to translate sentences
def translate(sentences, model, tokenizer):
    translated_sentences = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translated_sentence = tokenizer.decode(translated[0], skip_special_tokens=True)
        translated_sentences.append(translated_sentence)
    return translated_sentences

# Translate sentences to Hindi
hindi_sentences = translate(english_sentences, model, tokenizer)

# Create a DataFrame to display the translations
df = pd.DataFrame({'English': english_sentences, 'Hindi': hindi_sentences})

# Write the translations to a file
df.to_csv('translations.csv', index=False, encoding='utf-8')

print("Translations have been written to 'translations.csv'. Please open this file with a text editor that supports Unicode.")
