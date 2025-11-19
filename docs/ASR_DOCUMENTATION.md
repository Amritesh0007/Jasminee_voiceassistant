# Automatic Speech Recognition (ASR) Implementation

## Overview
This document describes the implementation of Automatic Speech Recognition (ASR) functionality in the Jasmine AI Assistant using Google Gemini API.

## Features
- Web-based speech recognition (existing)
- Google Gemini API-based speech recognition (new)
- Real-time audio recording and processing
- Support for multiple audio formats
- Integration with the existing GUI

## Implementation Details

### Backend Implementation
The ASR functionality is implemented in two modules:

1. **Backend/GeminiAPI.py** - Contains the core ASR functionality using Google Gemini
2. **Backend/SpeechToText.py** - Contains the audio recording and processing logic

> **Note**: Audio recording functionality requires PyAudio to be installed. If PyAudio is not available, the system will fall back to a simplified version that requires manually providing audio files.

### Key Functions

#### Gemini API ASR Function
```python
def speech_to_text(audio_file_path: str) -> Optional[str]:
    """
    Convert speech to text using Gemini's audio processing capabilities.
    
    Args:
        audio_file_path (str): Path to the audio file (WAV format recommended)
        
    Returns:
        Optional[str]: Transcribed text or None if failed
    """
```

#### Audio Recording Class
```python
class AudioRecorder:
    def __init__(self, filename="Data/recorded_audio.wav", format=pyaudio.paInt16, channels=1, rate=16000, chunk=1024):
        # Initialize audio recording parameters
    
    def start_recording(self):
        # Start recording audio
    
    def stop_recording(self):
        # Stop recording and save the audio file
```

#### Main ASR Function
```python
def GeminiSpeechRecognition():
    """
    Speech recognition using Google Gemini API
    """
```

## Usage

### From Command Line
```bash
python test_asr.py
```

### From GUI
1. Launch the Jasmine AI Assistant GUI
2. Click the "🎙️ GEMINI ASR" button
3. Speak into your microphone for 5 seconds
4. View the transcribed text

## Audio Format Support
- WAV (recommended)
- Other formats supported by Gemini API

## Configuration
The ASR functionality uses the existing Google Gemini API key configured in the `.env` file.

## Future Enhancements
- Continuous speech recognition
- Wake word detection
- Multi-language support
- Noise reduction preprocessing
- Custom vocabulary support

## Troubleshooting
- Ensure PyAudio is properly installed
- Check microphone permissions
- Verify Gemini API key is valid
- Confirm internet connectivity