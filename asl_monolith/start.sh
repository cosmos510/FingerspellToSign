#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Launch the Django app
echo "🚀 Starting ASL Recognition App..."
echo "📍 Make sure your webcam is connected!"
echo ""
python3 manage.py runserver
