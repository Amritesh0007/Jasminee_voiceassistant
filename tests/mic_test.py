#!/usr/bin/env python3
"""
Direct microphone test for Jasmine AI
"""
import speech_recognition as sr
import time

def test_microphone():
    print("🎙️ Direct Microphone Test")
    print("=" * 25)
    
    try:
        # Create recognizer
        r = sr.Recognizer()
        
        # List microphones
        print("Available microphones:")
        mic_names = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_names):
            print(f"  {i}: {name}")
        
        if not mic_names:
            print("❌ No microphones found!")
            return False
            
        # Use default microphone
        print("\nUsing default microphone (0)...")
        mic = sr.Microphone()
        
        with mic as source:
            print("🔊 Adjusting for ambient noise (2 seconds)...")
            r.adjust_for_ambient_noise(source, duration=2)
            print("✅ Ready! Please speak clearly for 3 seconds...")
            
            try:
                # Listen for 3 seconds
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                print("✅ Audio captured!")
                
                # Try to recognize speech
                print("🔄 Processing speech...")
                try:
                    text = r.recognize_google(audio)
                    print(f"📝 Recognized text: {text}")
                    print("✅ Microphone and speech recognition are working!")
                    return True
                except sr.UnknownValueError:
                    print("⚠️  Could not understand audio - try speaking more clearly")
                    return False
                except sr.RequestError as e:
                    print(f"❌ Recognition service error: {e}")
                    return False
                    
            except sr.WaitTimeoutError:
                print("⚠️  No speech detected - try speaking louder or closer to the microphone")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Jasmine AI Microphone Test")
    print("=" * 30)
    
    success = test_microphone()
    
    if success:
        print("\n🎉 Microphone is working correctly!")
        print("Try running the full application again.")
    else:
        print("\n🔧 Troubleshooting steps:")
        print("1. Check System Preferences > Security & Privacy > Privacy > Microphone")
        print("2. Ensure Terminal and Chrome have microphone permissions")
        print("3. Check that your microphone is not muted")
        print("4. Try speaking louder or closer to the microphone")
        print("5. Restart your terminal application")