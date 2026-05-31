@echo off
REM Quick start script for Windows

echo Starting Karwarian.shop development server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start server
python manage.py runserver 0.0.0.0:8000

pause
