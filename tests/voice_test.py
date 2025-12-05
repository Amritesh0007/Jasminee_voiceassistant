#!/usr/bin/env python3
"""
Simple voice recognition test script for Jasmine AI Assistant
"""
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_voice_recognition():
    """Test the voice recognition functionality"""
    print("🎙️ Jasmine AI Voice Recognition Test")
    print("=" * 40)
    
    try:
        # Import the speech recognition module
        from Backend.SpeechToText import SpeechRecognition
        print("✓ SpeechRecognition module imported successfully")
        
        print("\n📝 Testing voice recognition...")
        print("Please speak after the prompt appears.")
        print("The test will wait for 10 seconds for your voice input.")
        print("\n⚠️  Make sure:")
        print("  1. Chrome browser will open automatically")
        print("  2. Allow microphone access when prompted")
        print("  3. Click 'Start Recognition' in the browser")
        print("  4. Speak clearly after clicking the button")
        print("\nStarting test in 3 seconds...")
        
        time.sleep(3)
        
        # Try to capture voice input
        print("🎤 Listening for voice input (10 seconds)...")
        result = SpeechRecognition()
        print(f"📝 Recognition result: {result}")
        
        if result:
            print("✅ Voice recognition is working!")
            return True
        else:
            print("❌ No voice input detected")
            return False
            
    except Exception as e:
        print(f"❌ Error during voice recognition test: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_permissions():
    """Check if required permissions are granted"""
    print("\n🔐 Permission Check")
    print("=" * 20)
    
    import platform
    if platform.system() == "Darwin":  # macOS
        print("Please verify these permissions in System Preferences:")
        print("1. Security & Privacy > Privacy > Microphone")
        print("   - Terminal.app should be checked")
        print("   - Google Chrome should be checked")
        print("2. Security & Privacy > Privacy > Accessibility")
        print("   - Terminal.app (if available)")
    else:
        print("Please ensure your terminal has microphone access")

if __name__ == "__main__":
    print("Jasmine AI Voice Recognition Diagnostic")
    print("=" * 45)
    
    # Run the test
    success = test_voice_recognition()
    
    # Check permissions
    check_permissions()
    
    if success:
        print("\n🎉 Voice recognition is working correctly!")
        print("You should now be able to use voice commands with Jasmine AI.")
    else:
        print("\n🔧 Troubleshooting steps:")
        print("1. Check microphone permissions for Chrome and Terminal")
        print("2. Ensure your microphone is not muted")
        print("3. Try running the full application: python Main.py")
        print("4. Check if there's background noise interfering")
        print("5. Speak clearly and at a moderate pace")