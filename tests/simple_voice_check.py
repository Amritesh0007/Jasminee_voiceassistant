#!/usr/bin/env python3
"""
Simple voice input test for Jasmine AI Assistant
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_microphone_access():
    """Check if we can access the microphone directly"""
    print("🎤 Microphone Access Test")
    print("=" * 25)
    
    try:
        import pyaudio
        import wave
        
        # Test microphone access
        p = pyaudio.PyAudio()
        
        # Try to open microphone stream
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("✓ Microphone access successful")
        
        # Try to read a small amount of data
        data = stream.read(1024)
        print("✓ Microphone data capture successful")
        
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return True
        
    except Exception as e:
        print(f"❌ Microphone access failed: {e}")
        return False

def check_speech_recognition_library():
    """Check if speech recognition library is working"""
    print("\n🗣️ Speech Recognition Library Test")
    print("=" * 30)
    
    try:
        import speech_recognition as sr
        
        # Test recognizer
        recognizer = sr.Recognizer()
        print("✓ SpeechRecognition library imported successfully")
        print("✓ Recognizer created successfully")
        
        return True
    except Exception as e:
        print(f"❌ SpeechRecognition library error: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n⚙️ Environment Variables Check")
    print("=" * 28)
    
    try:
        from dotenv import dotenv_values
        env_vars = dotenv_values(".env")
        
        required_vars = ["InputLanguage"]
        missing_vars = []
        
        for var in required_vars:
            if var in env_vars and env_vars[var]:
                print(f"✓ {var}: {env_vars[var]}")
            else:
                print(f"⚠️ {var}: Not set")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ Environment variables check failed: {e}")
        return False

def main():
    """Run all checks"""
    print("Jasmine AI Voice Input Diagnostic")
    print("=" * 35)
    
    checks = [
        check_microphone_access,
        check_speech_recognition_library,
        check_environment_variables
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 35)
    print("📊 Diagnostic Summary")
    print("=" * 35)
    
    if all(results):
        print("✅ All checks passed! Voice input should work.")
        print("\nTry these steps:")
        print("1. Run: python Main.py")
        print("2. When Chrome opens, click 'Start Recognition'")
        print("3. Speak clearly into your microphone")
        print("4. Check if text appears in the Chrome window")
    else:
        print("❌ Some checks failed. Voice input may not work.")
        print("\nTroubleshooting steps:")
        print("1. Check microphone permissions in System Preferences")
        print("2. Ensure Terminal and Chrome have microphone access")
        print("3. Check if your microphone is not muted")
        print("4. Try running: pip install pyaudio speechrecognition")
        print("5. Restart your terminal application")

if __name__ == "__main__":
    main()