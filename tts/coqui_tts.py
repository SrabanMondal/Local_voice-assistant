import pyaudio
import wave
import os
from TTS.api import TTS

# Initialize Coqui TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak_text(text, stop_event=None):
    """
    Convert text to speech using Coqui TTS and play the audio.
    
    Args:
        text (str): Text to synthesize and speak.
        stop_event (threading.Event, optional): If set, stops playback early.
    """
    output_file = "assets/output.wav"
    tts.tts_to_file(text=text, file_path=output_file)

    with wave.open(output_file, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        chunk = 1024
        data = wf.readframes(chunk)
        while data and (stop_event is None or not stop_event.is_set()):
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Cleaned up {output_file}")