import sys
import ollama
from config import OLLAMA_MODEL, OLLAMA_HOST
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from utils.commands import handle_command

def main():
    """
    Main loop for TARS voice assistant.
    Listens for voice commands, processes them (basic or via Ollama), and responds via speech.
    """
    print("TARS: Initializing...")
    # Initialize Ollama client
    client = ollama.Client(host=OLLAMA_HOST)
    # Pre-warm the model
    try:
        print("TARS: Warming up model...")
        client.generate(model=OLLAMA_MODEL, prompt="Hello", options={'timeout': 30})
        print("TARS: Model ready.")
    except Exception as e:
        print(f"TARS: Model warmup failed: {e}. Proceeding anyway.")
    console_mode = "--console" in sys.argv
    if console_mode:
        print("TARS: Console mode. Type commands (type 'exit' to quit).")
    else:
        print("TARS: Ready. Say 'hello' to start.")

    while True:
        if console_mode:
            command = input("You: ").strip()
        else:
            command = listen()
        if command:
            response = handle_command(command)
            if response is None:
                # Use Ollama for advanced queries
                print("TARS: Thinking...")
                try:
                    result = client.generate(model=OLLAMA_MODEL, prompt=command, options={'timeout': 60})
                    response = result['response'].strip()
                    print(f"TARS: Response received: {response[:50]}...")
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"
                    print(f"TARS: Error: {e}")
            if console_mode:
                print(f"TARS: {response}")
            else:
                speak(response)
            if "shutting down" in response.lower():
                break
        # If no command, continue listening

if __name__ == "__main__":
    main()