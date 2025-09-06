#!/bin/bash

# Start FastAPI Server Script
# This script properly sets up the Python path and starts the server

echo "🚀 Starting FastAPI Server..."
echo "📍 Current directory: $(pwd)"
echo "🔧 Activating virtual environment..."

# Activate the virtual environment
source /Users/guruduttjangid/ai-job-readiness/.venv/bin/activate

echo "✅ Virtual environment activated"
echo "🔧 Setting PYTHONPATH..."

# Set the Python path to include the current directory
export PYTHONPATH="/Users/guruduttjangid/ai-job-readiness/backend:$PYTHONPATH"

echo "✅ PYTHONPATH set to: $PYTHONPATH"
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Auto-reload enabled"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
