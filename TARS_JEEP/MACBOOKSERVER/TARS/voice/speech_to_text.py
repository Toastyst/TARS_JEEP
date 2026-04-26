import speech_recognition as sr
from config import ENERGY_THRESHOLD, PAUSE_THRESHOLD

def listen():
    """
    Captures audio from microphone and converts to text using Google Speech Recognition.
    Returns the transcribed text or None if failed.
    """
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD
    r.pause_threshold = PAUSE_THRESHOLD

    with sr.Microphone() as source:
        print("TARS: Listening...")
        try:
            audio = r.listen(source, timeout=5)  # Timeout after 5 seconds of silence
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("TARS: No speech detected.")
            return None
        except sr.UnknownValueError:
            print("TARS: Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"TARS: Could not request results; {e}")
            return None