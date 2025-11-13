@echo off
echo ========================================
echo MySQL Setup for AI News Agency
echo ========================================
echo.

echo Step 1: Starting MySQL service...
net start MySQL
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not start MySQL service.
    echo Please start MySQL manually from Services (services.msc)
    echo Or check if MySQL is installed.
    pause
    exit /b 1
)

echo.
echo Step 2: Please create the database manually:
echo.
echo Run these commands:
echo   mysql -u root -p
echo   CREATE DATABASE ai_news_agency CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo   EXIT;
echo.
pause

echo.
echo Step 3: Running database migrations...
cd backend
alembic upgrade head
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Migrations failed. Please check database connection.
    pause
    exit /b 1
)

cd ..
echo.
echo ========================================
echo MySQL Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart backend server
echo 2. Go to http://localhost:3000
echo 3. Search for news (articles will be saved to database)
echo 4. Click "Process with AI" button
echo.
pause

