from faster_whisper import WhisperModel
import pyttsx3
import ollama
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
import time

# === CONFIG - change these two lines only ===
OLLAMA_MODEL = "gemma4:e2b"     # or "llama3.2:1b" for maximum speed
STT_SIZE     = "tiny"          # "tiny" = fastest, "base" = better accuracy

print("🎙️  TARS Voice Test Bench ready")
print(f"   Model: {OLLAMA_MODEL} | STT: {STT_SIZE}")
print("   Say 'quit' or press Ctrl+C to stop\n")

# Load once
stt = WhisperModel(STT_SIZE, device="cpu", compute_type="int8")
tts = pyttsx3.init()
tts.setProperty('rate', 180)   # speaking speed - tweak if you want

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
        audio = record(6)
        text = transcribe(audio)
        if not text or len(text) < 2:
            continue

        print(f"You: {text}")
        if "quit" in text.lower() or "exit" in text.lower():
            break

        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": text}]
        )
        reply = resp["message"]["content"].strip()
        print(f"TARS: {reply}\n")

        tts.say(reply)
        tts.runAndWait()

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(0.5)