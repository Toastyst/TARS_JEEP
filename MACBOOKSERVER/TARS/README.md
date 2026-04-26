# TARS Voice Assistant

A voice-controlled AI assistant powered by Ollama, inspired by the robot from Interstellar.

## Quick Start

1. **Install Ollama Model**:
   - Run `pull_model.bat` to download gemma4:e2b (models stored on E: drive)

2. **Install Dependencies**:
   - Run `install.bat` to install Python packages

3. **Run TARS**:
   - Run `start_tars.bat` to start Ollama server and TARS (all-in-one)

(Alternatively, run `start_ollama.bat` then `run.bat`, or use terminal commands as listed in Troubleshooting)

## Features

- **Voice Input**: Speak commands via microphone
- **Voice Output**: Responses spoken aloud
- **Basic Commands**: Time, date, greetings
- **AI Queries**: Advanced questions handled by Ollama (gemma4:e2b)

## Usage Guide

- Start by saying "Hello" or "Hi"
- Ask questions like "What is the weather?" (uses Ollama)
- Basic commands:
  - "What time is it?" → Current time
  - "What is today's date?" → Current date
  - "Goodbye", "Exit", or "Shutdown" → Stops the assistant
- The assistant listens continuously; speak clearly

## Testing

- **Console Mode**: `python main.py --console` for text-based testing (no mic/TTS).
- **Model Tests**: `python test_model.py` runs automated checks on commands and Ollama responses.

## Configuration

Edit `config.py` to customize:
- Ollama model/host
- Voice rate/volume
- Speech recognition thresholds

## Requirements

- Python 3.8+
- Microphone access
- Internet for speech recognition (Google API)

## Troubleshooting

- Ensure Ollama is running (`ollama serve`)
- Check microphone permissions
- For speech issues, adjust thresholds in `config.py`
- First Ollama query may take 1-5 minutes as the model loads (subsequent queries are faster)
- If TARS freezes, check Ollama server status or restart
