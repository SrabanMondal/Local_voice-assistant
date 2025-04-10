from stt.whisper_fast import transcribe_audio
from model.model import generate_text
from tts.coqui_tts import speak_text

def main():
    print("🎤 Listening...")
    text = transcribe_audio()  # e.g., "Hola, ¿cómo estás?"

    print("🧠 Translating...")
    translated = generate_text(text, target_lang="en")  # → "Hello, how are you?"
    print('Translated text-',translated)
    print("🗣️ Speaking...")
    speak_text(translated)

if __name__ == "__main__":
    main()
