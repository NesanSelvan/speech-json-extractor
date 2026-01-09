from pywhispercpp.model import Model
import time
model = Model('medium', n_threads=6)

def speech_to_text(path):
    startTime = time.time()
    segments = model.transcribe(path, extract_probability=True)
    endTime = time.time()
    full_text = []
    for segment in segments:
        print(f"{segment.text} (prob: {segment.probability:.2f})")
        # if segment.probability == segment.probability and segment.probability < 0.3:
        #     continue
        full_text.append(segment.text)
    print(f"Transcription completed in {endTime - startTime:.2f} seconds")
    return " ".join(full_text)

speech_to_text("nesan.ogg")