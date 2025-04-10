import asyncio
import threading
import pyaudio
import numpy as np
from stt.whisper_fast import transcribe_audio
from model.model import generate_text
from tts.coqui_tts import speak_text
import pvporcupine

async def listen_and_transcribe():
    """
    Listen for audio and transcribe (2s chunk).
    Returns transcribed text or None if empty.
    """
    print("🎤 Listening...")
    try:
        text = transcribe_audio()
        return text.strip() if text else None
    except Exception as e:
        print(f"STT error: {e}")
        return None

async def speak_with_wake_word(text, stop_event, wake_detected):
    """
    Speak text, pause if wake word is detected.
    Returns True if completed, False if paused.
    """
    print("🗣️ Speaking...")
    try:
        # Start wake word detection
        porcupine = pvporcupine.create(
            access_key="aY/khpizoxuGPZj3q+4S7dHk3mcwd5cg4F4CVeAWyX7KcMkNdvbVxA==",
            keyword_paths=["assets/hades.ppn"]
        )
        pa = pyaudio.PyAudio()
        wake_stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=porcupine.sample_rate,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        # Speak in thread, check wake word
        speak_thread = threading.Thread(target=speak_text, args=(text, stop_event))
        speak_thread.start()

        while speak_thread.is_alive() and not stop_event.is_set():
            pcm = wake_stream.read(porcupine.frame_length, exception_on_overflow=False)
            if len(pcm) == 0:
                continue
            pcm = np.frombuffer(pcm, dtype=np.int16)
            if porcupine.process(pcm) >= 0:  # Wake word detected
                stop_event.set()
                wake_detected.set()
                break
            await asyncio.sleep(0.01)  # Yield

        speak_thread.join()
        wake_stream.stop_stream()
        wake_stream.close()
        pa.terminate()
        porcupine.delete()

        return not stop_event.is_set()
    except Exception as e:
        print(f"TTS/Wake error: {e}")
        return False

async def main():
    stop_event = threading.Event()  # Signal to pause TTS
    wake_detected = threading.Event()  # Signal wake word detected

    while True:
        stop_event.clear()
        wake_detected.clear()

        # Listen for query
        input_text = await listen_and_transcribe()
        if not input_text:
            print("No input, listening again...")
            continue
        if input_text.lower().startswith("hey ai"):
            print("Wake word detected, listening for command...")
            input_text = input_text[6:].strip() or (await listen_and_transcribe()) or ""

        print(f"Transcribed: {input_text}")

        # Generate response
        print("🧠 Processing...")
        response_text = generate_text(input_text, target_lang="en")
        print(f"Response: {response_text}")

        # Speak with wake word detection
        completed = await speak_with_wake_word(response_text, stop_event, wake_detected)
        if not completed and wake_detected.is_set():
            print("Wake word interrupted, listening...")
            continue

if __name__ == "__main__":
    asyncio.run(main())