"""
Live Speech-to-Text Module with Speaker Verification
"""
import pyaudio
import numpy as np
import threading
import time
import queue
from collections import deque
import sys
import os
import wave
from typing import Callable, Optional, Any, Union

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Make webrtcvad import optional
WEBRTC_VAD_AVAILABLE = False
webrtcvad = None
try:
    import webrtcvad
    WEBRTC_VAD_AVAILABLE = True
except ImportError:
    print("Warning: webrtcvad not available. Install with: pip install webrtcvad")

# Try to import faster-whisper for local STT
WHISPER_AVAILABLE = False
WhisperModel = None
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    print("Warning: faster-whisper not available. Install with: pip install faster-whisper")

# Try to import Google Gemini for cloud STT
GEMINI_AVAILABLE = False
gemini_api = None
try:
    from Backend.GeminiAPI import gemini_api
    GEMINI_AVAILABLE = gemini_api is not None and hasattr(gemini_api, 'model') and gemini_api.model is not None
except ImportError:
    pass

# Import torch only if needed
torch = None
try:
    import torch
except ImportError:
    pass

class LiveSpeechToText:
    def __init__(self, speaker_verifier=None, stt_backend="whisper"):
        """
        Initialize Live Speech-to-Text
        
        Args:
            speaker_verifier: Speaker verification instance
            stt_backend (str): STT backend ("whisper" or "gemini")
        """
        self.speaker_verifier = speaker_verifier
        self.stt_backend = stt_backend.lower()
        self.is_recording = False
        self.audio_thread = None
        self.text_callback: Optional[Callable] = None
        self.final_text_callback: Optional[Callable] = None
        self.user_id = "myself"
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1600  # 0.1 seconds at 16kHz
        self.format = pyaudio.paInt16
        self.channels = 1
        
        # VAD for silence detection
        if WEBRTC_VAD_AVAILABLE and webrtcvad is not None:
            self.vad = webrtcvad.Vad(2)
        else:
            self.vad = None
        self.silence_threshold = 30  # frames of silence to detect end
        self.silence_counter = 0
        self.speech_buffer = deque(maxlen=100)  # Buffer for speech segments
        
        # Initialize STT model
        self.stt_model = None
        self._initialize_stt_model()
        
        # Audio buffer for continuous recognition
        self.audio_buffer = np.array([], dtype=np.int16)
        self.partial_text = ""
        
    def _initialize_stt_model(self):
        """Initialize the STT model based on selected backend"""
        if self.stt_backend == "whisper" and WHISPER_AVAILABLE and WhisperModel is not None:
            try:
                # Initialize Whisper model (small model for balance of speed and accuracy)
                self.stt_model = WhisperModel("small", device="cpu", compute_type="int8")
                print("Whisper STT model initialized")
            except Exception as e:
                print(f"Error initializing Whisper model: {e}")
                self.stt_model = None
        elif self.stt_backend == "gemini" and GEMINI_AVAILABLE:
            print("Using Gemini for STT")
            # For Gemini, we don't store a model object, just use the gemini_api directly
            self.stt_model = None  # We'll use gemini_api directly in _transcribe_with_gemini
        else:
            print(f"STT backend {self.stt_backend} not available")
            self.stt_model = None
    
    def _is_speech(self, audio_chunk):
        """Check if audio chunk contains speech using VAD"""
        # If webrtcvad is not available, use a simple energy-based approach
        if not WEBRTC_VAD_AVAILABLE or self.vad is None:
            # Simple energy-based VAD as fallback
            try:
                if isinstance(audio_chunk, np.ndarray):
                    audio_data = audio_chunk
                else:
                    audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
                
                # Calculate energy (RMS)
                energy = np.sqrt(np.mean(audio_data**2))
                # Simple threshold for voice activity detection
                return energy > 0.01
            except Exception:
                # If energy calculation fails, assume it's speech
                return True
        
        try:
            # Convert to bytes for VAD
            if isinstance(audio_chunk, np.ndarray):
                audio_bytes = audio_chunk.tobytes()
            else:
                audio_bytes = audio_chunk
            
            # VAD requires 10, 20, or 30 ms frames
            frame_duration = 20  # ms
            frame_samples = int(self.sample_rate * frame_duration / 1000)
            
            # Process in 20ms frames
            for i in range(0, len(audio_bytes), frame_samples * 2):  # *2 for 16-bit samples
                frame = audio_bytes[i:i + frame_samples * 2]
                if len(frame) == frame_samples * 2:
                    try:
                        if self.vad.is_speech(frame, self.sample_rate):
                            return True
                    except Exception:
                        pass
            return False
        except Exception:
            # If VAD fails, assume it's speech
            return True
    
    def _transcribe_with_whisper(self, audio_data):
        """Transcribe audio using Whisper"""
        # Check if we have a valid Whisper model
        if not self.stt_model or not WHISPER_AVAILABLE or not hasattr(self.stt_model, 'transcribe'):
            return ""
        
        try:
            # Convert to float32 numpy array
            if isinstance(audio_data, np.ndarray):
                if audio_data.dtype != np.float32:
                    audio_float = audio_data.astype(np.float32) / 32768.0
                else:
                    audio_float = audio_data
            else:
                audio_float = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe
            segments, info = self.stt_model.transcribe(audio_float, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return ""
    
    def _transcribe_with_gemini(self, audio_data):
        """Transcribe audio using Google Gemini"""
        if not GEMINI_AVAILABLE or gemini_api is None or not hasattr(gemini_api, 'model') or not gemini_api.model:
            return ""
        
        try:
            # Save audio to temporary file
            temp_file = "temp_speech.wav"
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data)
            
            # Transcribe with Gemini
            if hasattr(gemini_api, 'speech_to_text'):
                result = gemini_api.speech_to_text(temp_file)
            else:
                result = ""
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            return result if result else ""
        except Exception as e:
            print(f"Gemini transcription error: {e}")
            return ""
    
    def _process_audio_chunk(self, audio_chunk):
        """Process an audio chunk: verify speaker and transcribe if valid"""
        # Verify speaker
        if self.speaker_verifier:
            verification_result = self.speaker_verifier.verify_speaker(self.user_id, audio_chunk)
            if not verification_result["accept"]:
                # Speaker not verified, ignore
                if self.text_callback:
                    # Try calling with two arguments first
                    try:
                        self.text_callback("[Voice not recognized]", False)
                    except TypeError:
                        # Fallback to single argument
                        self.text_callback("[Voice not recognized]")
                return
        
        # Check for speech
        if not self._is_speech(audio_chunk):
            # Increment silence counter
            self.silence_counter += 1
            # If enough silence, finalize transcription
            if self.silence_counter >= self.silence_threshold and len(self.audio_buffer) > 0:
                self._finalize_transcription()
            return
        else:
            # Reset silence counter when speech is detected
            self.silence_counter = 0
        
        # Add to speech buffer
        if isinstance(audio_chunk, np.ndarray):
            self.audio_buffer = np.concatenate([self.audio_buffer, audio_chunk])
        else:
            chunk_array = np.frombuffer(audio_chunk, dtype=np.int16)
            self.audio_buffer = np.concatenate([self.audio_buffer, chunk_array])
        
        # Transcribe if buffer is large enough (every 1 second)
        if len(self.audio_buffer) >= self.sample_rate:
            self._transcribe_buffer()
    
    def _transcribe_buffer(self):
        """Transcribe the current audio buffer"""
        if len(self.audio_buffer) == 0:
            return
        
        try:
            # Transcribe with selected backend
            if self.stt_backend == "whisper" and self.stt_model is not None:
                text = self._transcribe_with_whisper(self.audio_buffer)
            elif self.stt_backend == "gemini":
                text = self._transcribe_with_gemini(self.audio_buffer.tobytes())
            else:
                text = ""
            
            if text:
                self.partial_text = text
                if self.text_callback:
                    # Try calling with two arguments first
                    try:
                        self.text_callback(text, True)
                    except TypeError:
                        # Fallback to single argument
                        self.text_callback(text)
                    
        except Exception as e:
            print(f"Transcription error: {e}")
    
    def _finalize_transcription(self):
        """Finalize transcription and clear buffer"""
        if len(self.audio_buffer) > 0:
            # Transcribe remaining audio
            self._transcribe_buffer()
            
            # Call final text callback
            if self.final_text_callback and self.partial_text:
                self.final_text_callback(self.partial_text)
            
            # Clear buffer and reset
            self.audio_buffer = np.array([], dtype=np.int16)
            self.partial_text = ""
            self.silence_counter = 0
    
    def set_text_callback(self, callback: Callable):
        """
        Set callback for partial text updates
        
        Args:
            callback: Function that takes (text, is_verified) or (text) as parameters
        """
        self.text_callback = callback
    
    def set_final_text_callback(self, callback: Callable):
        """
        Set callback for final text (when user stops speaking)
        
        Args:
            callback: Function that takes (text) as parameter
        """
        self.final_text_callback = callback
    
    def start_stream(self):
        """Start audio streaming and transcription"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.audio_thread = threading.Thread(target=self._audio_capture_loop, daemon=True)
        self.audio_thread.start()
        print("Live STT started")
    
    def stop_stream(self):
        """Stop audio streaming and transcription"""
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join(timeout=1.0)
        self._finalize_transcription()
        print("Live STT stopped")
    
    def _audio_capture_loop(self):
        """Main audio capture loop"""
        try:
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            
            # Open stream
            stream = p.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print("Audio stream opened")
            
            # Capture loop
            while self.is_recording:
                try:
                    # Read audio chunk
                    audio_chunk = stream.read(self.chunk_size, exception_on_overflow=False)
                    
                    # Process chunk
                    self._process_audio_chunk(audio_chunk)
                    
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    time.sleep(0.01)  # Brief pause to prevent busy loop
            
            # Clean up
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except Exception as e:
            print(f"Error in audio capture loop: {e}")

# Example usage
if __name__ == "__main__":
    # Create STT instance
    stt = LiveSpeechToText()
    
    # Set callbacks
    def on_text_update(text, is_verified=True):
        if is_verified:
            print(f"Partial: {text}")
        else:
            print("[Voice not recognized]")
    
    def on_final_text(text):
        print(f"Final: {text}")
    
    stt.set_text_callback(on_text_update)
    stt.set_final_text_callback(on_final_text)
    
    # Start streaming
    stt.start_stream()
    
    try:
        # Record for 30 seconds
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        stt.stop_stream()