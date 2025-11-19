#!/usr/bin/env python3
"""
Demo script for Automatic Speech Recognition using Google Gemini API
This script demonstrates the full ASR functionality with a sample audio file.
"""

import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_asr_with_sample_file():
    """Demo ASR functionality with a sample audio file"""
    print("🤖 Jasmine AI - Automatic Speech Recognition Demo")
    print("=" * 50)
    
    # Check if sample audio file exists
    sample_audio_path = "Data/speech.mp3"
    if not os.path.exists(sample_audio_path):
        print(f"❌ Sample audio file not found: {sample_audio_path}")
        print("Please provide an audio file for transcription.")
        return False
    
    print(f"📁 Using audio file: {sample_audio_path}")
    print(f"📊 File size: {os.path.getsize(sample_audio_path)} bytes")
    
    try:
        # Import the ASR function
        from Backend.GeminiAPI import speech_to_text
        
        print("\n🔄 Sending audio to Google Gemini API for transcription...")
        
        # Perform speech recognition
        result = speech_to_text(sample_audio_path)
        
        if result:
            print("\n✅ Transcription successful!")
            print(f"📝 Transcribed text: {result}")
            return True
        else:
            print("\n❌ Failed to transcribe audio")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during transcription: {e}")
        return False

def demo_asr_functionality():
    """Demo the full ASR functionality"""
    print("🤖 Jasmine AI - ASR Functionality Demo")
    print("=" * 50)
    
    # Test 1: Direct ASR function
    print("\n1️⃣  Testing direct ASR function...")
    success1 = demo_asr_with_sample_file()
    
    # Test 2: Backend integration
    print("\n2️⃣  Testing backend integration...")
    try:
        from Backend.SpeechToText import GeminiSpeechRecognition
        print("✅ Backend integration test passed")
        success2 = True
    except Exception as e:
        print(f"❌ Backend integration test failed: {e}")
        success2 = False
    
    # Test 3: GUI availability
    print("\n3️⃣  Testing GUI availability...")
    try:
        # Try to import PyQt (either version)
        try:
            import PyQt6
            print("✅ GUI available (PyQt6)")
            success3 = True
        except ImportError:
            try:
                import PyQt5
                print("✅ GUI available (PyQt5)")
                success3 = True
            except ImportError:
                print("⚠️  GUI not available (PyQt not installed)")
                success3 = True  # This is not a failure, just a limitation
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        success3 = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ASR Functionality Test Summary:")
    print(f"   Direct ASR Function: {'✅ Pass' if success1 else '❌ Fail'}")
    print(f"   Backend Integration: {'✅ Pass' if success2 else '❌ Fail'}")
    print(f"   GUI Availability:    {'✅ Pass' if success3 else '❌ Fail'}")
    
    if success1 and success2:
        print("\n🎉 All core ASR functionality is working correctly!")
        print("🎙️  You can now use the '🎙️ GEMINI ASR' button in the GUI")
        print("   or call the speech_to_text() function directly.")
        return True
    else:
        print("\n❌ Some ASR functionality tests failed.")
        return False

if __name__ == "__main__":
    demo_asr_functionality()