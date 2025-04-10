import pyaudio
import wave
import numpy as np
from faster_whisper import WhisperModel

# Initialize Faster-Whisper model (loaded once for efficiency)
model = WhisperModel("base", device="cpu")

def transcribe_audio(use_test_file=False):
    if use_test_file:
        # Use test file for debugging
        segments, _ = model.transcribe("assets/input.wav", language="en")
        return " ".join([seg.text for seg in segments])

    # Record audio from microphone
    RATE = 16000  # Sample rate (Hz)
    CHUNK = 1024  # Buffer size
    RECORD_SECONDS = 5  # Duration to record

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Open stream
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording... Speak now!")
    frames = []

    # Record for specified duration
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recording to temporary WAV file
    temp_wav = "temp_audio.wav"
    with wave.open(temp_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Transcribe the temporary WAV file
    segments, _ = model.transcribe(temp_wav, language="en")
    text = " ".join([seg.text for seg in segments])
    print("Recognized text-",text)
    # Clean up temporary file (optional, comment out for debugging)
    import os
    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    return text