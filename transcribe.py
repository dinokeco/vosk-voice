import os
import sys
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def main():
    # Path to the Vosk model
    model_path = "model"
    
    if not os.path.exists(model_path):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{model_path}' in the current folder.")
        sys.exit(1)

    # Initialize the model
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    try:
        # Open the audio stream
        stream = p.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8000)
        stream.start_stream()

        print("Listening... Press Ctrl+C to stop.")

        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                # result is a JSON string
                result = json.loads(rec.Result())
                if result.get("text"):
                    print(f"Transcription: {result['text']}")
            else:
                # partial_result is also a JSON string
                partial = json.loads(rec.PartialResult())
                if partial.get("partial"):
                    # Use \r to overwrite the line for a live update feel
                    print(f"Partial: {partial['partial']}", end='\r')

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
