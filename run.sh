#!/bin/bash

# Personal Dashboard Runner Script

echo "🚀 Starting Personal Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/flask" ]; then
    echo "📚 Installing dependencies..."
    pip install -r requirements.txt
fi

# Create required directories
mkdir -p credentials tokens

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials before running!"
    exit 1
fi

# Check if Google credentials exist
if [ ! -f "credentials/google_credentials.json" ]; then
    echo "⚠️  Google credentials not found!"
    echo "Please download your OAuth credentials and save as:"
    echo "  credentials/google_credentials.json"
    echo ""
    echo "See QUICKSTART.md for instructions."
    exit 1
fi

# Start the application
echo "✨ Starting dashboard on http://localhost:5000"
python app.py
