@echo off
REM EduTrack Deployment Script for Windows

echo 🚀 EduTrack Deployment Script
echo =============================

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run database setup
echo 🗄️ Setting up database...
python -c "import database; database.create_tables()"

REM Run the application
echo 🌟 Starting EduTrack Web Application...
echo 📱 Open http://localhost:5000 in your browser
python web_app.py