import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def recognize_audio(file_path):
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I could not understand the audio."
            except sr.RequestError:
                return "Sorry, there was an error with the request."
    except FileNotFoundError:
        return f"File not found: {file_path}"

def speak_text(text, rate):
    engine.setProperty('rate', rate)  # Set to a slower rate
    engine.say(text)
    engine.runAndWait()

def custom_speak_text(text, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")
    os.system("start output.mp3")  # On Windows
    # os.system("mpg321 output.mp3")  # On Linux

# Use raw strings or double backslashes for paths
english_audio_path = r"C:\Users\Ankit Hutiya\englishwav.wav"
hindi_audio_path = r"C:\Users\Ankit Hutiya\hindiwav.wav"

# Recognize speech from English and Hindi samples
english_text = recognize_audio(english_audio_path)
hindi_text = recognize_audio(hindi_audio_path)

print(f"English text: {english_text}")
print(f"Hindi text: {hindi_text}")

# Convert recognized text to speech with adjusted rate
print("Speaking English text...")
speak_text(english_text, rate=145)  # Adjust the rate here

print("Speaking Hindi text...")
custom_speak_text(hindi_text, language='hi')
