#!/bin/bash
# Backend startup script

cd backend
uvicorn main:app --reload --port 8000

