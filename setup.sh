#!/bin/bash

# Universal Video Downloader Setup Script
# This script automates the setup process for both backend and frontend

set -e

echo "=========================================="
echo "Universal Video Downloader Setup"
echo "=========================================="
echo ""

# Check for required dependencies
echo "Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install npm."
    exit 1
fi

echo "✓ All required dependencies found"
echo ""

# Setup Backend
echo "=========================================="
echo "Setting up Backend..."
echo "=========================================="

cd video_downloader_backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Google Drive API credentials"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo "Initializing database..."
python src/main.py --init-db

echo "✓ Backend setup complete"
echo ""

# Setup Frontend
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="

cd ../video-downloader-frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Build frontend
echo "Building frontend..."
npm run build

# Copy to backend static folder
echo "Copying built files to backend..."
cp -r dist/* ../video_downloader_backend/src/static/

echo "✓ Frontend setup complete"
echo ""

# Final instructions
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "1. Navigate to video_downloader_backend directory"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run: python src/main.py"
echo "4. Open browser to: http://localhost:5000"
echo ""
echo "For Google Drive integration:"
echo "1. Edit video_downloader_backend/.env"
echo "2. Add your GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET"
echo "3. Restart the application"
echo ""
echo "Enjoy using Universal Video Downloader!"
echo "=========================================="
