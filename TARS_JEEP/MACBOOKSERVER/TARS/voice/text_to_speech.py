import pyttsx3
from config import VOICE_RATE, VOICE_VOLUME

engine = None

def init_engine():
    """
    Initializes the TTS engine if not already done.
    """
    global engine
    if engine is None:
        engine = pyttsx3.init()
        engine.setProperty('rate', VOICE_RATE)
        engine.setProperty('volume', VOICE_VOLUME)

def speak(text):
    """
    Converts text to speech and plays it.
    """
    init_engine()
    engine.say(text)
    engine.runAndWait()