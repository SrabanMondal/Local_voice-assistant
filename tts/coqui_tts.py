import pyaudio
import wave
from TTS.api import TTS

# Initialize Coqui TTS model (loaded once for efficiency)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak_text(text):
    """
    Convert text to speech using Coqui TTS and play the audio.
    
    Args:
        text (str): Text to synthesize and speak.
    """
    # Generate WAV file
    output_file = "assets/output.wav"
    tts.tts_to_file(text=text, file_path=output_file)
    print('Voice generated')
    # Play the WAV file using pyaudio
    with wave.open(output_file, 'rb') as wf:
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Open stream
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Read and play audio data
        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        # Cleanup
        print("Speak done")
        stream.stop_stream()
        stream.close()
        p.terminate()