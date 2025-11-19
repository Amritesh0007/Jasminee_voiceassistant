#!/usr/bin/env python3
"""
Real-time Automatic Speech Recognition using Google Gemini API
This script provides real-time audio recording and transcription.
"""

import os
import sys
import time
import threading

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def record_audio_cli(duration=5):
    """Record audio for a specified duration using PyAudio"""
    try:
        import pyaudio
        import wave
        
        # Audio recording parameters
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024
        RECORD_SECONDS = duration
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        # Start recording
        print(f"🔴 Recording for {duration} seconds... Speak now!")
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                           rate=RATE, input=True,
                           frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Stop recording
        print("⏹️  Recording finished!")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the recorded audio
        output_file = "Data/recorded_speech.wav"
        os.makedirs("Data", exist_ok=True)
        
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"💾 Audio saved to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Error recording audio: {e}")
        return None

def transcribe_audio(audio_file):
    """Transcribe audio file using Gemini API"""
    try:
        from Backend.GeminiAPI import speech_to_text
        print("🔄 Sending audio to Google Gemini API for transcription...")
        result = speech_to_text(audio_file)
        return result
    except Exception as e:
        print(f"❌ Error transcribing audio: {e}")
        return None

def real_time_asr(duration=5):
    """Main function for real-time ASR"""
    print("🎙️  Jasmine AI - Real-time Automatic Speech Recognition")
    print("=" * 55)
    print(f"Ready to record for {duration} seconds.")
    print("Press Enter to start recording...")
    
    input()
    
    # Record audio
    audio_file = record_audio_cli(duration)
    if not audio_file:
        print("❌ Failed to record audio")
        return
    
    # Transcribe audio
    transcription = transcribe_audio(audio_file)
    if transcription:
        print("\n✅ Transcription successful!")
        print(f"📝 Result: {transcription}")
    else:
        print("\n❌ Failed to transcribe audio")

def interactive_asr():
    """Interactive ASR with user-controlled recording duration"""
    print("🎙️  Jasmine AI - Interactive ASR")
    print("=" * 35)
    
    while True:
        try:
            duration = input("\nEnter recording duration in seconds (or 'quit' to exit): ")
            if duration.lower() == 'quit':
                break
            
            duration = int(duration)
            if duration <= 0:
                print("Please enter a positive number")
                continue
                
            real_time_asr(duration)
            
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
            real_time_asr(duration)
        except ValueError:
            print("Usage: python real_time_asr.py [duration_in_seconds]")
            print("Example: python real_time_asr.py 5")
    else:
        interactive_asr()