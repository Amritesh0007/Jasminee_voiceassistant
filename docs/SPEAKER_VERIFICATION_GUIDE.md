# Speaker Verification and Live Speech-to-Text Guide

This guide explains how to use the new speaker verification and live speech-to-text features in Jasmine AI.

## Overview

Jasmine AI now includes advanced voice recognition capabilities:
1. **Speaker Verification**: Recognizes only your voice and ignores others
2. **Live Speech-to-Text**: Real-time transcription of your speech
3. **GUI Integration**: Live transcription display in the assistant interface

## Setup Requirements

### 1. Install Additional Dependencies

You can install the required dependencies in two ways:

**Option A: Manual installation**
```bash
pip install speechbrain webrtcvad torch torchaudio scikit-learn
```

**Option B: Using the installation script**
```bash
python utils/install_voice_dependencies.py
```

For local speech-to-text (optional):
```bash
pip install faster-whisper
```

### 2. Enroll Your Voice

Before using speaker verification, you need to enroll your voice:

1. Record 3-10 WAV files of yourself speaking normally
2. Run the enrollment script:

```bash
python utils/enroll_voice.py myself sample1.wav sample2.wav sample3.wav
```

## How It Works

### Pipeline Architecture

```
Audio Input (chunk)
        ↓
Speaker Verification (ECAPA-TDNN)
        ↓ valid
Live STT (Whisper / Gemini)
        ↓
GUI Live Text Display
        ↓
Decision Model → Chatbot / Realtime Search / etc.
```

### Speaker Verification Process

1. Audio chunks are captured in real-time (16kHz, 1600 samples per 0.1 sec)
2. Each chunk is verified using SpeechBrain ECAPA-TDNN
3. If similarity score ≥ threshold (default 0.72) → accept
4. If similarity score < threshold → reject and ignore

### Live Speech-to-Text Options

1. **Faster Whisper** (local, offline):
   - Pros: Free, fast, no internet required
   - Cons: Uses CPU/GPU resources

2. **Google Gemini Live** (cloud):
   - Pros: Extremely accurate, easy streaming
   - Cons: Requires API key

## Usage Instructions

### 1. Voice Enrollment

```bash
# Enroll with 3-10 voice samples
python utils/enroll_voice.py myself voice1.wav voice2.wav voice3.wav

# The system will create an enrollment profile for "myself"
```

### 2. Running Live Speech-to-Text

The live STT is integrated into the main GUI. When you run:

```bash
python Main.py
```

The system will:
1. Start listening for audio input
2. Verify each audio chunk against enrolled voice
3. Transcribe verified speech in real-time
4. Display transcription in the GUI

### 3. Configuration

You can adjust the verification threshold in `SpeakerVerifier.py`:

```python
verifier = SpeakerVerifier(threshold=0.72)  # Default threshold
```

Higher values = more strict verification
Lower values = more permissive verification

## API Reference

### SpeakerVerifier Class

```python
from Backend.SpeakerVerifier import SpeakerVerifier

# Initialize
verifier = SpeakerVerifier(threshold=0.72)

# Enroll user
verifier.enroll_user("myself", ["voice1.wav", "voice2.wav"])

# Verify speaker
result = verifier.verify_speaker("myself", audio_chunk)
# Returns: {"accept": True/False, "score": similarity_score}
```

### LiveSpeechToText Class

```python
from Backend.LiveSpeechToText import LiveSpeechToText

# Initialize with speaker verifier
stt = LiveSpeechToText(speaker_verifier=verifier, stt_backend="whisper")

# Set callbacks
def on_text_update(text, is_verified):
    print(f"Live text: {text}")

def on_final_text(text):
    print(f"Final text: {text}")

stt.set_text_callback(on_text_update)
stt.set_final_text_callback(on_final_text)

# Start/stop streaming
stt.start_stream()
stt.stop_stream()
```

## Troubleshooting

### No Voice Recognition

1. Check that you've enrolled your voice properly
2. Verify WAV files are valid and accessible
3. Adjust threshold value in SpeakerVerifier

### Audio Issues

1. Ensure microphone is properly connected
2. Check system audio settings
3. Verify PyAudio is installed correctly

### Performance Issues

1. For better performance, use local Whisper with GPU support
2. Reduce audio chunk size for lower latency
3. Close other applications using audio resources

## Security Notes

- Voice profiles are stored locally
- No voice data is transmitted to external servers
- All processing happens on your device (unless using cloud STT)

## Limitations

- Speaker verification works best with consistent recording conditions
- Background noise may affect verification accuracy
- Requires sufficient voice samples for accurate enrollment

## Future Improvements

- Adaptive threshold adjustment
- Multi-speaker support
- Noise reduction preprocessing
- Enhanced GUI visualization