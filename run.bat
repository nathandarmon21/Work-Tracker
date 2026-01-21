@echo off
REM Personal Dashboard Runner Script for Windows

echo Starting Personal Dashboard...

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if dependencies are installed
if not exist "venv\Scripts\flask.exe" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Create required directories
if not exist "credentials\" mkdir credentials
if not exist "tokens\" mkdir tokens

REM Check if .env exists
if not exist ".env" (
    echo WARNING: No .env file found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env with your credentials before running!
    pause
    exit /b 1
)

REM Check if Google credentials exist
if not exist "credentials\google_credentials.json" (
    echo WARNING: Google credentials not found!
    echo Please download your OAuth credentials and save as:
    echo   credentials\google_credentials.json
    echo.
    echo See QUICKSTART.md for instructions.
    pause
    exit /b 1
)

REM Start the application
echo Starting dashboard on http://localhost:5000
python app.py
