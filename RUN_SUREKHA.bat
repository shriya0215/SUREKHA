@echo off
title SUREKHA - Housing Society Management Software
color 1F
echo.
echo  ============================================
echo       SUREKHA - Starting Server...           
echo  ============================================
echo.

:: Kill any existing python on port 5000
taskkill /F /IM python.exe >nul 2>&1

:: Change to app directory
cd /d "C:\Users\Rutuja\OneDrive\Desktop\MINI PROJECT\SocioNest"

:: Start Flask in background
start /B python app.py > server_log.txt 2>&1

:: Wait 3 seconds for server to start
timeout /t 3 /nobreak >nul

:: Open browser automatically
start "" "http://127.0.0.1:5000"

echo  [OK] SUREKHA is running at: http://127.0.0.1:5000
echo  [INFO] Close this window ONLY to stop the server.
echo.
pause
