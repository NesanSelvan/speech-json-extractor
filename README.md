# Speech JSON Extractor

Real-time speech-to-text with LLM-powered JSON extraction. Speak naturally and get structured data.

## Demo

https://github.com/user-attachments/assets/demo.mov

1. **Records** audio from your microphone
2. **Transcribes** speech using Whisper (pywhispercpp)
3. **Extracts** structured JSON using LLM (Gemma via LM Studio)

## Example

**You say:** "2 tomatoes, 3 onions, and 1 chicken"

**Output:**
```json
{"items": [{"name": "tomatoes", "quantity": 2}, {"name": "onions", "quantity": 3}, {"name": "chicken", "quantity": 1}]}
```

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

Press `Ctrl+C` to stop recording.

## Requirements

- Python 3.10+
- macOS (Apple Silicon recommended) / Linux
- LM Studio running locally with Gemma model
- Microphone access

### Install PortAudio (for PyAudio)

**macOS:**
```bash
brew install portaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
```

## Configuration

Edit `main.py` to change:
- `INPUT_DEVICE_INDEX` - Your microphone index
- `RATE` - Sample rate (default: 16000)

Edit `text_transcription.py` to change:
- `url` - LM Studio API endpoint
- `model` - LLM model name

## Project Structure

```
├── main.py                    # Main recording loop
├── audio_transcription_v2.py  # Whisper transcription
├── text_transcription.py      # LLM JSON extraction
└── requirements.txt           # Dependencies
```

## How It Works

1. Records 3-second audio chunks
2. Sends to Whisper for transcription
3. Sends transcription to LLM for JSON extraction
4. Displays results in real-time

## License

MIT