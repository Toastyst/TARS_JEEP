def handle_command(command):
    """
    Handles basic hardcoded commands.
    Returns a response string if command is recognized, else None to pass to Ollama.
    """
    cmd = command.lower()
    if "hello" in cmd or "hi" in cmd:
        return "Hello, I am TARS, your voice assistant."
    elif "time" in cmd:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in cmd:
        from datetime import datetime
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}."
    elif "goodbye" in cmd or "exit" in cmd or "shutdown" in cmd:
        return "Shutting down. Goodbye."
    else:
        return None  # Not a basic command, use Ollama