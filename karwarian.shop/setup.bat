@echo off
REM Karwarian.shop Setup Script for Windows

echo =========================================
echo Karwarian.shop Setup Script (Windows)
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created. Please update it with your settings.
)

REM Create necessary directories
echo Creating directories...
if not exist media\places mkdir media\places
if not exist media\news mkdir media\news
if not exist media\matrimony mkdir media\matrimony
if not exist media\jobs\companies mkdir media\jobs\companies
if not exist media\services mkdir media\services
if not exist static\images mkdir static\images

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
echo =========================================
echo Create Admin Superuser
echo =========================================
echo You'll need this to access the admin panel at /admin
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the development server:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Access the website at: http://127.0.0.1:8000
echo Access admin panel at: http://127.0.0.1:8000/admin
echo.
echo Press any key to start the server now...
pause

REM Start development server
python manage.py runserver
