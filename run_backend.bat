@echo off
REM Backend startup script for Windows

cd backend
uvicorn main:app --reload --port 8000

