#!/bin/bash
echo "Starting AI News Agency Servers..."
echo ""

echo "Starting Backend Server..."
cd "$(dirname "$0")"
python -m uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 3

echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Servers are starting..."
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop servers"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

wait

