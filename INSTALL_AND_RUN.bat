@echo off
title SUREKHA - Installing Dependencies
color 1F
echo ============================================
echo   SUREKHA - Setup and Install
echo ============================================
echo.
echo Step 1: Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit
)

echo.
echo Step 2: Installing Flask...
pip install flask

echo.
echo Step 3: Installing python-docx...
pip install python-docx

echo.
echo ============================================
echo   SETUP COMPLETE! Now launching SUREKHA...
echo ============================================
echo.
cd /d "%~dp0"
start "" python app.py
timeout /t 3 >nul
start "" http://127.0.0.1:5000
