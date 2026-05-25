@echo off
title नेपाल सरकार रोजगार सेवा - Nepal Government Job Service
color 1B

echo ============================================
echo  🇳🇵 नेपाल सरकार रोजगार सेवा
echo  Nepal Government Job Service Portal
echo ============================================
echo.
echo  Starting servers...
echo.

:: Activate venv
echo [1/3] Activating Python environment...
call "venv\Scripts\activate.bat"

:: Install requirements
echo [2/3] Installing dependencies...
pip install -r requirements.txt -q

:: Start the FastAPI backend (real scrapers populate jobs on startup)
echo.
echo ============================================
echo  ✅ Starting servers!
echo  🌐 Backend:     http://127.0.0.1:8000
echo  🏛️  Nepal Portal: http://127.0.0.1:8000/nepal
echo  🌍 Global Portal: http://127.0.0.1:8000/global
echo  📊 Docs:        http://127.0.0.1:8000/docs
echo ============================================
echo.
python backend/main.py

pause
