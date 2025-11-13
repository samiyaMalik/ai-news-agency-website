@echo off
echo ========================================
echo Starting AI News Agency Application
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server (Port 8000)...
start "Backend Server" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo ✅ Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul

