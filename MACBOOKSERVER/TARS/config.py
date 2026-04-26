# Configuration for TARS voice assistant

# Ollama settings
OLLAMA_MODEL = "gemma4:e2b"
OLLAMA_HOST = "http://localhost:11434"  # Default Ollama server

# Voice settings (for pyttsx3)
VOICE_RATE = 200  # Words per minute
VOICE_VOLUME = 1.0  # 0.0 to 1.0

# Speech recognition settings
ENERGY_THRESHOLD = 300  # Minimum audio energy to consider for recording
PAUSE_THRESHOLD = 0.8  # Seconds of non-speaking audio before a phrase is considered complete