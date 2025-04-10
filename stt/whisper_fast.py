import pyaudio
import wave
import numpy as np
import os
from faster_whisper import WhisperModel

# Initialize Faster-Whisper model
model = WhisperModel("base", device="cpu")  # Faster for Pi

def transcribe_audio(use_test_file=False):
    """
    Record audio from microphone or use a test file and transcribe it to text.
    
    Args:
        use_test_file (bool): If True, transcribe assets/input.wav instead of recording.
    
    Returns:
        str: Transcribed text from the audio.
    """
    if use_test_file:
        segments, _ = model.transcribe("assets/input.wav", language="en")
        return " ".join([seg.text for seg in segments])

    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 3

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording... Speak now!")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    temp_wav = "temp_audio.wav"
    with wave.open(temp_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    segments, _ = model.transcribe(temp_wav, language="en")
    text = " ".join([seg.text for seg in segments])

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    return text