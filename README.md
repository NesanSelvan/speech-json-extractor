# Live Microphone to Whisper Transcription

A real-time speech-to-text application that captures live audio from your microphone and transcribes it using OpenAI's Whisper model.

## Features

- 🎙️ **Real-time microphone capture** - Live audio recording from your microphone
- 🎵 **Whisper transcription** - High-quality speech recognition using OpenAI Whisper
- ⚡ **Low-latency processing** - 3-second audio chunks for near real-time transcription
- 🔇 **Voice activity detection** - Automatically filters out silence
- 💾 **Auto-save transcriptions** - All transcriptions saved to timestamped files
- 🎛️ **Audio device selection** - Choose from available microphones
- 🧵 **Multi-threaded processing** - Separate threads for recording and transcription
- ✅ **Clean error handling** - Graceful handling of audio and transcription errors

## Quick Setup

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Activate the virtual environment:**
   ```bash
   source speech_env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the live transcription:**
   ```bash
   python main.py
   ```

## Manual Setup (Alternative)

If you prefer to set up manually:

1. **Create virtual environment:**
   ```bash
   python3 -m venv speech_env
   source speech_env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Select audio device** (optional):
   - The app will list all available microphones
   - By default, it uses your system's default microphone
   - To use a specific device, modify the `device_index` in the code

3. **Start speaking:**
   - The app will capture and transcribe your speech in real-time
   - Transcriptions appear with timestamps
   - Processing time is shown for each transcription

4. **Stop and save:**
   - Press `Ctrl+C` to stop recording
   - All transcriptions are automatically saved to a timestamped text file

## Configuration Options

### Whisper Model Sizes
You can change the model in `main.py`:
- `tiny` - Fastest, least accurate (~39 MB)
- `base` - Good balance, default (~74 MB)
- `small` - Better accuracy (~244 MB)
- `medium` - High accuracy (~769 MB)
- `large` - Best accuracy, slowest (~1550 MB)

### Audio Settings
- **Sample Rate**: 16kHz (optimal for Whisper)
- **Channels**: Mono (single channel)
- **Chunk Duration**: 3 seconds (configurable)
- **Audio Format**: 16-bit PCM

### Voice Activity Detection
- Automatically filters out silent audio chunks
- Adjustable volume threshold in the code
- Prevents transcription of background noise

## System Requirements

- **Python 3.7+**
- **macOS, Linux, or Windows**
- **Microphone access**
- **Internet connection** (for initial Whisper model download)
- **Audio drivers** (PortAudio for PyAudio)

### macOS Installation Notes
If you encounter PyAudio installation issues on macOS:
```bash
brew install portaudio
pip install pyaudio
```

### Linux Installation Notes
If you encounter PyAudio installation issues on Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## Output Files

Transcriptions are automatically saved as:
- **Filename**: `transcription_YYYYMMDD_HHMMSS.txt`
- **Format**: Timestamped text with processing times
- **Location**: Same directory as the script

## Troubleshooting

### Common Issues

1. **PyAudio installation errors**:
   - Install PortAudio system dependency first
   - Use appropriate package manager for your OS

2. **No microphone detected**:
   - Check microphone permissions
   - Verify microphone is not in use by other applications
   - Try running with different audio device index

3. **Slow transcription**:
   - Use a smaller Whisper model (tiny or base)
   - Reduce chunk duration
   - Ensure sufficient system resources

4. **Poor transcription quality**:
   - Use a larger Whisper model (medium or large)
   - Improve microphone quality/positioning
   - Reduce background noise

### Performance Tips

- **CPU Usage**: Larger models require more processing power
- **Memory**: Ensure sufficient RAM for model loading
- **Real-time Factor**: Aim for transcription time < chunk duration
- **Audio Quality**: Use a good microphone for better results

## Advanced Usage

### Custom Audio Device
```python
# List devices first to find the index
transcriber.list_audio_devices()

# Use specific device
transcriber.start_recording(device_index=2)
```

### Adjust Processing Parameters
```python
# Create with different settings
transcriber = LiveWhisperTranscriber(
    model_size="small",     # Better accuracy
    chunk_duration=5.0      # Longer chunks for context
)
```

## Technical Details

- **Audio Processing**: 16-bit PCM at 16kHz sample rate
- **Threading**: Separate threads for recording and transcription
- **Queue Management**: Thread-safe audio and transcription queues
- **Overlap Processing**: 50% overlap between audio chunks for continuity
- **Error Recovery**: Graceful handling of audio stream interruptions

## License

This project uses OpenAI's Whisper model under MIT license.

## Contributing

Feel free to submit issues and enhancement requests!