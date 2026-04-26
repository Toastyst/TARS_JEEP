# TARS_JEEP

A small test bench for validating TARS VTT speech-to-text (STT) integration.

## Description

This repository contains tools for testing TARS VTT STT workflows, including the main script `tars_test_bench.py`.

## Requirements

- Python 3.10 or newer
- `ollama` installed and configured for your local model
- Audio input/output support on your system

## Dependencies

Install the required Python packages from `requirements.txt` with:

```powershell
python -m pip install -r requirements.txt
```

### Windows notes

- `faster-whisper` depends on `av` (PyAV), which may require a prebuilt wheel or build tools.
- If import errors occur, install a wheel-compatible version of `av` or use:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install av
```

- `faster-whisper` also needs `ffmpeg` available on the system PATH for audio decoding.

If you encounter audio device issues on macOS, make sure your microphone and speakers are enabled and accessible.

## Debug logging

The script writes a debug log to `tars_test_bench.log` in the repository root. Check this file for detailed information about STT transcription, Ollama responses, and TTS engine state.

## Usage

1. Install the required dependencies above.
2. Run `python tars_test_bench.py`.
3. Speak into the microphone and review the printed output.
4. Say `quit` or press `Ctrl+C` to stop.

## Configuration

Edit the config section in `tars_test_bench.py` to customize:

- `OLLAMA_MODEL`: Ollama model (e.g., "gemma4:e2b")
- `STT_SIZE`: Whisper model size ("tiny", "base", etc.)
- `TTS_VOICE`: Voice name substring (e.g., "David")
- `SYSTEM_PROMPT`: System message for Ollama (TARS persona)
- `RECORD_SECONDS`: Audio recording duration (seconds)
- `TTS_RATE`: Speech rate (words per minute)

## Voice Configuration

This project uses the **David** male voice (Windows system voice) for TARS character dialogue. The voice is optimized for:
- Low latency and edge efficiency on light hardware
- Clear, authoritative tone suitable for TARS
- Zero additional dependencies or network requirements

On Windows, the voice is "Microsoft David Desktop - English (United States)". If not available, install via Settings > Time & Language > Speech > Manage voices.

The script logs available voices and configs on startup.

## Notes

- Originally developed for macOS, but the repository can be adapted for other platforms.
- Keep `tars_test_bench.py` and related test assets in sync with your TARS configuration.

