@echo off
echo Starting AI News Agency Servers...
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Servers are starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul

