import threading
import time
from stt.whisper_fast import transcribe_with_pause
from model.model import generate_text
from tts.coqui_tts import speak_text_stream

def stt_llm_thread(text_container, stop_event):
    """
    Thread for continuous STT and LLM processing.
    Updates text_container with response, sets stop_event on 'stop'.
    """
    while True:
        stop_event.clear()
        # Listen with pause detection
        input_text = transcribe_with_pause()
        if not input_text:
            continue
        
        if input_text.lower().strip() == "stop":
            print("Stop cmd: ",input_text)
            stop_event.set()
            continue

        print(f"Transcribed: {input_text}")
        
        # Generate response
        print("🧠 Processing...",input_text)
        response_text = generate_text(input_text, target_lang="en")
        print(f"Response: {response_text}")
        
        # Set shared text for TTS
        with text_container["lock"]:
            text_container["value"] = response_text

def tts_thread(text_container, stop_event):
    """
    Thread for TTS, checks text_container, streams text, stops on stop_event.
    """
    while True:
        # Check for text or stop
        with text_container["lock"]:
            text = text_container["value"]
        
        if text and len(text)>0 and not stop_event.is_set():
            print("🗣️ Speaking...")
            speak_text_stream(text, stop_event)
            # Clear text after speaking or stop
            with text_container["lock"]:
                text_container["value"] = ""
                stop_event.clear()
        else:
            time.sleep(0.3)  # Avoid busy-waiting

def main():
    # Shared variables
    text_container = {"value": "", "lock": threading.Lock()}
    stop_event = threading.Event()

    # Start threads
    print("Thread starting")
    stt_llm = threading.Thread(target=stt_llm_thread, args=(text_container, stop_event))
    tts = threading.Thread(target=tts_thread, args=(text_container, stop_event))
    
    stt_llm.daemon = True
    tts.daemon = True
    
    stt_llm.start()
    tts.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()

if __name__ == "__main__":
    main()