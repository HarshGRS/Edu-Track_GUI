#!/bin/bash
# EduTrack Deployment Script

echo "🚀 EduTrack Deployment Script"
echo "============================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # Linux/Mac

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run database setup
echo "🗄️  Setting up database..."
python -c "import database; database.create_tables()"

# Run the application
echo "🌟 Starting EduTrack Web Application..."
echo "📱 Open http://localhost:5000 in your browser"
python web_app.py