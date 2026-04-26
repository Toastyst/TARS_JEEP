import logging
from faster_whisper import WhisperModel
import pyttsx3
import ollama
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
import time

# === CONFIG - change these lines as needed ===
OLLAMA_MODEL = "gemma4:e2b"     # or "llama3.2:1b" for maximum speed
STT_SIZE     = "tiny"          # "tiny" = fastest, "base" = better accuracy
TTS_VOICE    = "David"         # Male voice suitable for TARS character
SYSTEM_PROMPT = "You are TARS, a witty and efficient AI companion from Interstellar. Respond helpfully and in character."
RECORD_SECONDS = 6
TTS_RATE = 180
LOG_FILE     = "tars_test_bench.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("TARS Voice Test Bench ready")
logger.info(f"Model: {OLLAMA_MODEL} | STT: {STT_SIZE}")
logger.info(f"Configs: Voice={TTS_VOICE}, Record={RECORD_SECONDS}s, TTS Rate={TTS_RATE}")
logger.info("Say 'quit' or press Ctrl+C to stop")

# Load once
stt = WhisperModel(STT_SIZE, device="cpu", compute_type="int8")
logger.debug("Loaded Whisper STT model")

def init_tts_engine():
    engine = pyttsx3.init()
    try:
        voices = engine.getProperty('voices')
        logger.info(f"Available voices: {[v.name for v in voices]}")
        for voice in voices:
            if TTS_VOICE.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                logger.info(f"Using voice: {voice.name}")
                return engine
        logger.warning(f"Voice '{TTS_VOICE}' not found, using default")
    except Exception as e:
        logger.warning(f"Error setting voice: {e}, using default")
    engine.setProperty('rate', TTS_RATE)
    return engine


def speak(text):
    logger.debug("TTS speak called")
    for attempt in range(2):
        engine = init_tts_engine()
        try:
            logger.info(f"Speaking reply ({len(text)} chars), attempt {attempt + 1}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            logger.debug("TTS finished speak call")
            return
        except Exception as exc:
            logger.warning(f"TTS engine error on attempt {attempt + 1}: {exc}")
            try:
                engine.stop()
            except Exception as stop_exc:
                logger.debug(f"Error stopping TTS engine: {stop_exc}")
            if attempt == 1:
                logger.error("TTS failed after retry")
                raise
            time.sleep(0.1)


def record(seconds=6):
    print("🎤 Listening...")
    fs = 16000
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio.flatten()

def transcribe(audio):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        path = f.name
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())
    segments, _ = stt.transcribe(path, beam_size=1)
    text = " ".join(s.text for s in segments).strip()
    os.unlink(path)
    return text

while True:
    try:
        audio = record(RECORD_SECONDS)
        text = transcribe(audio)
        logger.debug(f"Transcribed text: {text!r}")
        if not text or len(text) < 2:
            logger.info("No valid transcription received, listening again")
            continue

        print(f"You: {text}")
        logger.info(f"User prompt: {text}")
        if "quit" in text.lower() or "exit" in text.lower():
            break

        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]
        )
        logger.debug(f"Received Ollama response object: {resp}")
        reply = resp["message"]["content"].strip()
        logger.info(f"Reply text: {reply}")
        print(f"TARS: {reply}\n")

        speak(reply)

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(0.5)