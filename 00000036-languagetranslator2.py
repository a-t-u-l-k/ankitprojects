from transformers import MarianMTModel, MarianTokenizer

# Initialize the model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-hi'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate sentences
def translate(sentence, model, tokenizer):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    translated_sentence = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_sentence

# Interactive loop for translating sentences
def main():
    print("Enter an English sentence to translate to Hindi (or type 'exit' to quit):")
    while True:
        english_sentence = input("English: ")
        if english_sentence.lower() == 'exit':
            break
        hindi_translation = translate(english_sentence, model, tokenizer)
        print(f"Hindi: {hindi_translation}")

if __name__ == "__main__":
    main()
