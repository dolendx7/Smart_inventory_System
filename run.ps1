# Smart Inventory System PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "       Starting Smart Inventory System (InvenLogic)     " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Check if MySQL is running on port 3306
$portOpen = (Get-NetTCPConnection -LocalPort 3306 -ErrorAction SilentlyContinue)
if (-not $portOpen) {
    Write-Host "[1/3] Starting MySQL Server..." -ForegroundColor Yellow
    Start-Process -FilePath "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" `
        -ArgumentList "--datadir=`"$env:LOCALAPPDATA\MySQL\data`" --port=3306" `
        -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/3] MySQL Server is already running." -ForegroundColor Green
}

# 2. Check virtual environment
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "[2/3] Setting up Python virtual environment..." -ForegroundColor Yellow
    py -m venv venv
    .\venv\Scripts\pip install -r requirements.txt
} else {
    Write-Host "[2/3] Virtual environment ready." -ForegroundColor Green
}

# 3. Launch browser and application
Write-Host "[3/3] Launching Web Application on http://127.0.0.1:5001 ..." -ForegroundColor Green
Start-Process "http://127.0.0.1:5001"
Write-Host ""
Write-Host "Application is running! Press CTRL+C to stop." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" app.py
