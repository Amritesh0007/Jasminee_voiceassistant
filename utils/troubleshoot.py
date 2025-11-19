#!/usr/bin/env python3
"""
Troubleshooting script for Jarvis AI Assistant
"""

import os
import sys
from dotenv import dotenv_values

def check_environment():
    """Check environment variables and configuration"""
    print("🔍 Checking Environment Configuration")
    print("=" * 40)
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file found")
        env_vars = dotenv_values(".env")
        print(f"   Username: {env_vars.get('Username', 'Not set')}")
        print(f"   Assistant Name: {env_vars.get('Assistantname', 'Not set')}")
        print(f"   Input Language: {env_vars.get('InputLanguage', 'Not set')}")
        print(f"   Cohere API Key: {'Set' if env_vars.get('CohereAPIKey') else 'Not set'}")
        print(f"   Groq API Key: {'Set' if env_vars.get('GroqAPIKey') else 'Not set'}")
    else:
        print("❌ .env file not found")
        return False
    
    return True

def check_directories():
    """Check required directories and files"""
    print("\n📂 Checking Directories and Files")
    print("=" * 40)
    
    # Check Data directory
    if os.path.exists("Data"):
        print("✅ Data directory exists")
        files = os.listdir("Data")
        print(f"   Files in Data: {files}")
    else:
        print("❌ Data directory not found")
    
    # Check Frontend/Files directory
    frontend_files_dir = os.path.join("Frontend", "Files")
    if os.path.exists(frontend_files_dir):
        print("✅ Frontend/Files directory exists")
        files = os.listdir(frontend_files_dir)
        print(f"   Files in Frontend/Files: {files}")
        
        # Check specific files
        mic_file = os.path.join(frontend_files_dir, "Mic.data")
        if os.path.exists(mic_file):
            with open(mic_file, "r") as f:
                mic_status = f.read().strip()
            print(f"   Microphone status: {mic_status}")
        else:
            print("   ❌ Mic.data file not found")
    else:
        print("❌ Frontend/Files directory not found")
    
    return True

def check_dependencies():
    """Check required Python packages"""
    print("\n📦 Checking Python Dependencies")
    print("=" * 40)
    
    required_packages = [
        "selenium",
        "webdriver_manager",
        "groq",
        "cohere",
        "pygame",
        "pyttsx3",
        "SpeechRecognition",
        "mtranslate",
        "PyQt6",
        "googlesearch-python",
        "beautifulsoup4",
        "rich",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip3 install " + " ".join(missing_packages))
    
    return len(missing_packages) == 0

def check_microphone():
    """Check microphone status and provide instructions"""
    print("\n🎤 Microphone Status")
    print("=" * 40)
    
    frontend_files_dir = os.path.join("Frontend", "Files")
    mic_file = os.path.join(frontend_files_dir, "Mic.data")
    
    if os.path.exists(mic_file):
        with open(mic_file, "r") as f:
            mic_status = f.read().strip()
        print(f"Current microphone status: {mic_status}")
        
        if mic_status.lower() == "true":
            print("✅ Microphone is active")
            print("   Speak clearly into your microphone now")
        else:
            print("⚠️  Microphone is inactive")
            print("   Run: python3 toggle_microphone.py true")
    else:
        print("❌ Mic.data file not found")
        print("   Run the application first to create it")

def main():
    """Main troubleshooting function"""
    print("🤖 Jarvis AI Assistant Troubleshooting")
    print("=" * 50)
    
    checks = [
        check_environment(),
        check_directories(),
        check_dependencies(),
        check_microphone()
    ]
    
    print("\n📋 Summary")
    print("=" * 40)
    print("✅ All checks completed")
    print("\n💡 Tips for voice interaction:")
    print("   1. Make sure your microphone is working and has proper permissions")
    print("   2. Speak clearly and at a moderate pace")
    print("   3. The first time you speak, Chrome may ask for microphone permission")
    print("   4. Check the terminal for status updates")
    print("   5. Responses will appear in the GUI and be spoken aloud")

if __name__ == "__main__":
    main()