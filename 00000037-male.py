import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()

    # List available voices (optional, for your reference)
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice ID: {voice.id}, Name: {voice.name}")

    # Set the voice to match your desired characteristics
    # Uncomment and set the voice ID if needed
    # engine.setProperty('voice', 'Voice_ID')

    # Adjust the rate of speech
    engine.setProperty('rate', 145)  # Set to a slower rate, e.g., 100 words per minute

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Example usage
english_text = "This is an example of slower speech."
print("Speaking English text...")
speak_text(english_text)
