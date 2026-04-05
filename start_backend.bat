@echo off
echo ========================================
echo Starting Enterprise Search Backend
echo ========================================
echo.

call venv\Scripts\activate.bat
cd backend
python main.py
