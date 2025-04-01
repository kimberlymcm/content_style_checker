#!/bin/bash

# Kill any existing uvicorn processes
pkill -f uvicorn

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload 