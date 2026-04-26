@echo off
set OLLAMA_MODELS=%~dp0..\ollama
echo Starting Ollama server...
start cmd /k "ollama serve"
echo Ollama server started in new window.
pause