import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    
    # List available voices
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice ID: {voice.id}, Name: {voice.name}")

    # Set the voice to match your desired gender and characteristics
    # Replace 'Voice_ID' with the actual ID from the available voices
    engine.setProperty('voice', 'Voice_ID')
    
    # Adjust the rate of speech
    engine.setProperty('rate', 150)  # Set to a value that suits your needs
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()
