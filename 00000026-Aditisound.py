import boto3
from pydub import AudioSegment
from pydub.playback import play
import os

# Text of the Indian National Anthem
national_anthem = """
जन गण मन अधिनायक जय हे, भारत भाग्य विधाता
पंजाब सिंधु गुजरात मराठा, द्राविड़ उत्कल बंग
विन्ध्य हिमाचल यमुना गंगा, उच्छल जलधि तरंग
तव शुभ नामे जागे, तव शुभ आशिष मागे
गाहे तव जय गाथा
जन गण मंगलदायक जय हे, भारत भाग्य विधाता
जय हे, जय हे, जय हे
जय जय जय जय हे
"""

# AWS credentials (replace these with your actual credentials)
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
region_name = 'ap-south-1'  # Example AWS region

# Initialize a session using Amazon Polly
polly = boto3.client(
    'polly',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Request speech synthesis
response = polly.synthesize_speech(
    Text=national_anthem,
    OutputFormat='mp3',
    VoiceId='Aditi'  # Use 'Aditi' for an Indian English voice (female)
)

# Set the file path for saving the audio file
output_dir = os.path.expanduser("~\\Desktop")  # This points to the user's Desktop
file_path = os.path.join(output_dir, "national_anthem.mp3")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the audio stream returned by Amazon Polly on your system
with open(file_path, 'wb') as file:
    file.write(response['AudioStream'].read())

# Load the audio file using pydub
audio = AudioSegment.from_mp3(file_path)

# Save the audio file in a format that `playsound` can play
audio.export(os.path.join(output_dir, "national_anthem.wav"), format="wav")

# Play the audio file
play(audio)
