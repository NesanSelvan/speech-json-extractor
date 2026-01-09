import os
os.environ["HF_HOME"] = os.path.join(os.getcwd(), "venv", "hf_cache")
from faster_whisper import WhisperModel, download_model
import psutil
import threading
import time
import os

model_size = "medium"
print(f"Downloading model {model_size}...")
model_path = download_model(model_size)
print(f"Model downloaded to {model_path}")

print("Loading model...")
model = WhisperModel(model_path, device="cpu", compute_type="int8")

print("Starting transcription...")



def transcribe_audio(path):
    start_time = time.time()
    segments, info = model.transcribe(
        path, 
        language="en",  
        beam_size=5,
        condition_on_previous_text=False,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        hallucination_silence_threshold=0.5,
        no_speech_threshold=0.6,
    )
    end_time = time.time()
    print(f"Transcription completed in {end_time - start_time:.2f} seconds")
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    startTime = time.time()
    
    full_text = []
    print("\n[Transcribing segments...]")
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        full_text.append(segment.text)

    endTime = time.time()
    print(f"Text transcription completed in {endTime - startTime:.2f} seconds")
    
    return " ".join(full_text)


