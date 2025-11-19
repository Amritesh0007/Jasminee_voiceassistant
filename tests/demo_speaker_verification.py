#!/usr/bin/env python3
"""
Demo script for speaker verification and live speech-to-text
"""
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_speaker_verification():
    """Demonstrate speaker verification functionality"""
    print("🎤 Speaker Verification Demo")
    print("=" * 30)
    
    try:
        from Backend.SpeakerVerifier import SpeakerVerifier
        
        # Create verifier
        verifier = SpeakerVerifier()
        print("✅ Speaker Verifier initialized")
        print(f"✅ Default threshold: {verifier.threshold}")
        
        # Show available methods
        print("\nAvailable methods:")
        print("- enroll_user(user_id, wav_files_list)")
        print("- verify_speaker(user_id, audio_chunk)")
        print("- set_threshold(threshold)")
        
        print("\nℹ️  To use speaker verification:")
        print("1. Record WAV files of your voice")
        print("2. Run: python utils/enroll_voice.py myself voice1.wav voice2.wav")
        print("3. Verification will automatically filter out other voices")
        
    except ImportError as e:
        print(f"❌ Speaker verification not available: {e}")
        print("💡 Install with: pip install speechbrain webrtcvad")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_live_speech_to_text():
    """Demonstrate live speech-to-text functionality"""
    print("\n🎙️ Live Speech-to-Text Demo")
    print("=" * 30)
    
    try:
        from Backend.LiveSpeechToText import LiveSpeechToText
        
        # Create STT instance
        stt = LiveSpeechToText()
        print("✅ Live Speech-to-Text initialized")
        print(f"✅ Backend: {stt.stt_backend}")
        
        # Show available methods
        print("\nAvailable methods:")
        print("- start_stream()")
        print("- stop_stream()")
        print("- set_text_callback(callback)")
        print("- set_final_text_callback(callback)")
        
        # Check available backends
        try:
            from faster_whisper import WhisperModel
            print("✅ Faster Whisper available for local STT")
        except ImportError:
            print("ℹ️  Faster Whisper not available (optional)")
            
        try:
            from Backend.GeminiAPI import gemini_api
            if gemini_api.model:
                print("✅ Google Gemini available for cloud STT")
            else:
                print("ℹ️  Google Gemini not configured (API key required)")
        except ImportError:
            print("ℹ️  Google Gemini not available")
            
    except ImportError as e:
        print(f"❌ Live STT not available: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_integration():
    """Demonstrate integration of both features"""
    print("\n🔗 Integration Demo")
    print("=" * 30)
    
    try:
        from Backend.SpeakerVerifier import SpeakerVerifier
        from Backend.LiveSpeechToText import LiveSpeechToText
        
        # Create instances
        verifier = SpeakerVerifier()
        stt = LiveSpeechToText(speaker_verifier=verifier)
        
        print("✅ Speaker verification integrated with live STT")
        print("✅ Pipeline: Audio → Speaker Verification → Speech-to-Text")
        
        # Show how the integration works
        print("\nHow it works:")
        print("1. Audio chunks captured in real-time")
        print("2. Each chunk verified against enrolled voice")
        print("3. Only verified audio is transcribed")
        print("4. Transcription displayed in GUI")
        print("5. Verified text sent to AI for processing")
        
    except Exception as e:
        print(f"❌ Integration demo failed: {e}")

def main():
    """Run all demos"""
    print("Jasmine AI - Speaker Verification and Live STT Demo")
    print("=" * 55)
    print("This demo shows the new voice recognition capabilities\n")
    
    demo_speaker_verification()
    demo_live_speech_to_text()
    demo_integration()
    
    print("\n" + "=" * 55)
    print("🎉 Demo completed!")
    print("\nNext steps:")
    print("1. Enroll your voice: python utils/enroll_voice.py myself *.wav")
    print("2. Run the full system: python Main.py")
    print("3. Speak to the assistant - only your voice will be recognized!")

if __name__ == "__main__":
    main()