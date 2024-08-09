from pydub import AudioSegment
from pydub.generators import Sine

# Parameters
duration_ms = 3000  # Duration of the tone in milliseconds
frequency = 440  # Frequency of the tone (A4 pitch)

# Generate a sine wave tone
tone = Sine(frequency).to_audio_segment(duration=duration_ms)

# Export the generated tone as a WAV file
tone.export("sine_wave_tone.wav", format="wav")

print("3-second sine wave tone generated and saved as 'sine_wave_tone.wav'")
