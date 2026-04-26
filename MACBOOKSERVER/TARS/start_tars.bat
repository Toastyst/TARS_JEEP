@echo off
set OLLAMA_MODELS=%~dp0..\ollama
echo Checking if Ollama is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% == 0 (
    echo Ollama is already running.
) else (
    echo Starting Ollama server...
    start "Ollama Server" cmd /k "ollama serve"
    echo Waiting for Ollama to start...
    timeout /t 10 /nobreak > nul
)
echo Starting TARS voice assistant...
python main.py
pause
