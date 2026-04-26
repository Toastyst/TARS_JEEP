@echo off
set OLLAMA_MODELS=%~dp0..\ollama
echo Pulling Ollama model gemma4:e2b...
ollama pull gemma4:e2b
echo Model pulled successfully.
pause
