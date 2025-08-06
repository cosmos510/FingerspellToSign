#!/usr/bin/env python3
"""
ASL Recognition App Setup Script
Simple setup for recruiters and demo purposes
"""
import os
import sys
import subprocess

def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up ASL Recognition App...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations core", "Creating core migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Running migrations"):
        sys.exit(1)
    
    # Create superuser (optional)
    print("\n📝 You can create a superuser account (optional):")
    print("Run: python manage.py createsuperuser")
    
    print("\n🎉 Setup complete!")
    print("🌐 To start the server, run: python manage.py runserver")
    print("📱 Then visit: http://localhost:8000")

if __name__ == "__main__":
    main()