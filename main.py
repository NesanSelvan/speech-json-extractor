from audio_transcription_v2 import speech_to_text
from text_transcription import transcribe_text
import pyaudio
import wave
import time
import signal
import sys
import threading
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
OUTPUT_FILENAME = "recorded_audio.wav"
INPUT_DEVICE_INDEX = 1

p = None
stream = None
frames = []
is_recording = True
transcription_lock = threading.Lock()
is_transcribing = False

def save_current_audio():
    global frames
    with transcription_lock:
        if not frames:
            return None
        chunks_per_3_seconds = int(RATE / CHUNK * 3)
        temp_frames = frames[-chunks_per_3_seconds:].copy()
    
    temp_file = "temp_recording.wav"
    wf = wave.open(temp_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(temp_frames))
    wf.close()
    return temp_file

def transcribe_current():
    global is_transcribing
    is_transcribing = True
    temp_file = save_current_audio()
    if temp_file:
        try:
            text = speech_to_text(temp_file)
            if text and text.strip() and not any(marker in text.upper() for marker in ['BLANK_AUDIO', 'INAUDIBLE', 'SILENCE']):
                text_format = transcribe_text(text)
                print(f"\nTranscription: {text_format}")
            else:
                print(f"\n(silence)")
            print(f"\rRecording...", end="", flush=True)
        except Exception as e:
            print(f"\nTranscription error: {e}")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    is_transcribing = False

def save_and_exit(signum=None, frame=None):
    global p, stream, frames, is_recording
    
    is_recording = False
    print("\n\nStopping recording...")
    
    if stream:
        stream.stop_stream()
        stream.close()
    
    if frames and p:
        wf = wave.open(OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        duration = len(frames) * CHUNK / RATE
        print(f"Audio saved to {OUTPUT_FILENAME} ({duration:.1f} seconds)")
        
        print("\nFinal transcription...")
        audio_text = speech_to_text(OUTPUT_FILENAME)
        print(f"\nFinal: {audio_text}")
        
        print("\nProcessing with LLM...")
        result = transcribe_text(audio_text)
        print(f"\nResult: {result}")
    
    if p:
        p.terminate()
    
    sys.exit(0)

print("Whisper model loaded!")

signal.signal(signal.SIGINT, save_and_exit)
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

print("Recording started... Press Ctrl+C to stop.")
print("-" * 60)

chunk_count = 0
start_time = time.time()

while is_recording:
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        with transcription_lock:
            frames.append(data)
        chunk_count += 1
        if chunk_count % (int(RATE / CHUNK) * 3) == 0 and not is_transcribing:
            elapsed = time.time() - start_time
            print(f"\rRecording: {elapsed:.0f}s - Transcribing...", end="", flush=True)
            t = threading.Thread(target=transcribe_current)
            t.start()
    except Exception as e:
        print(f"\nAudio error: {e}")
        continue
