import os
import time
import uuid
from gtts import gTTS
from pydub import AudioSegment
from pygame import mixer
from termcolor import colored
from tqdm import tqdm

def get_user_input(prompt):
    return input(colored(prompt, 'blue')).strip()

def show_progress(message):
    print(colored(message, 'yellow'))
    for _ in tqdm(range(100), desc="Progress", unit="file"):
        time.sleep(0.01)
    print()

def play_audio(file_path):
    try:
        mixer.init()  # Initialize the mixer module from pygame
        mixer.music.load(file_path)
        mixer.music.play()
        
        # Wait until the audio has finished playing
        while mixer.music.get_busy():
            time.sleep(1)
            
        # Ensure the mixer is stopped
        mixer.music.stop()
    except Exception as e:
        print(colored(f"Error during playback: {e}", 'red'))
    finally:
        mixer.quit()  # Quit the mixer module

def main():
    output_dir = "D:\\Projects\\Produced Sound"
    os.makedirs(output_dir, exist_ok=True)

    while True:
        # Get user input for the text they want to hear
        text_to_speak = get_user_input("What would you like to hear today? (Enter your text or 'exit' to quit): ")
        
        if text_to_speak.lower() == 'exit':
            print(colored("Exiting the program. Goodbye!", 'yellow'))
            break

        # Generate a unique file name for the temporary audio file
        unique_id = str(uuid.uuid4())
        temp_mp3_path = os.path.join(output_dir, f"temp_audio_{unique_id}.mp3")
        temp_wav_path = temp_mp3_path.replace(".mp3", ".wav")

        # Create an audio object for the input text using gTTS
        tts = gTTS(text=text_to_speak, lang='hi', slow=False, tld='co.in')

        # Save the audio to a file
        show_progress("Creating audio file...")
        tts.save(temp_mp3_path)

        # Load the audio file
        audio = AudioSegment.from_mp3(temp_mp3_path)

        # Ask if the user wants to hear the audio or just save it
        hear_option = get_user_input("Do you want to hear the audio now? (yes/no): ").lower()
        if hear_option == 'yes':
            print(colored("Playing the audio...", 'green'))
            audio.export(temp_wav_path, format="wav")
            play_audio(temp_wav_path)

        # Ask if the user wants to save the output file in a specific format
        save_option = get_user_input("Do you want to save this audio file? (yes/no): ").lower()
        
        if save_option == 'yes':
            format_choice = get_user_input("Enter the format you want to save the file in (mp3/wav): ").lower()
            file_name = get_user_input("Enter the file name (without extension): ").strip()
            final_file_path = os.path.join(output_dir, f"{file_name}.{format_choice}")

            # Save the audio file in the chosen format
            show_progress(f"Saving audio file as {final_file_path}...")
            audio.export(final_file_path, format=format_choice)
            print(colored(f"Audio file saved as {final_file_path}", 'green'))

        # Clean up temporary files
        try:
            if os.path.exists(temp_mp3_path):
                os.remove(temp_mp3_path)
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
        except Exception as e:
            print(colored(f"Error cleaning up temporary files: {e}", 'red'))

        # Ask if the user wants to hear more sounds
        more_sounds = get_user_input("Do you want to hear more sounds? (yes/no): ").lower()
        if more_sounds != 'yes':
            print(colored("Exiting the program. Goodbye!", 'yellow'))
            break

if __name__ == "__main__":
    main()
