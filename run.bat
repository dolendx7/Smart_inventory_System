@echo off
title Smart Inventory System Launcher
echo ========================================================
echo         Starting Smart Inventory System (InvenLogic)
echo ========================================================

:: Check if MySQL is already running on port 3306
netstat -ano | findstr :3306 >nul
if %errorlevel% neq 0 (
    echo [1/3] Starting MySQL Server...
    start "" /b "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" --datadir="%LOCALAPPDATA%\MySQL\data" --port=3306
    timeout /t 3 /nobreak >nul
) else (
    echo [1/3] MySQL Server is already running.
)

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [2/3] Setting up Python virtual environment...
    py -m venv venv
    venv\Scripts\pip install -r requirements.txt
) else (
    echo [2/3] Virtual environment ready.
)

:: Launch the Flask application
echo [3/3] Launching Web Application on http://127.0.0.1:5001 ...
start http://127.0.0.1:5001
echo.
echo Application is running! Press CTRL+C in this window to stop.
echo ========================================================
venv\Scripts\python.exe app.py
pause
