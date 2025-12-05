"""
Speaker Verification Module using SpeechBrain ECAPA-TDNN
"""
import os
import torch
import torchaudio
import numpy as np
import wave
from speechbrain.pretrained import EncoderClassifier
from sklearn.metrics.pairwise import cosine_similarity

class SpeakerVerifier:
    def __init__(self, threshold=0.72):
        """
        Initialize the Speaker Verifier
        
        Args:
            threshold (float): Similarity threshold for verification
        """
        self.threshold = threshold
        self.classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.enrollments = {}
        # Remove webrtcvad dependency and use a simple energy-based VAD
        self.vad_energy_threshold = 0.01  # Energy threshold for voice activity detection
        
    def _normalize_audio(self, audio_data, sample_rate=16000):
        """
        Normalize audio data to float32 and ensure correct sample rate
        
        Args:
            audio_data: Audio data (numpy array or tensor)
            sample_rate: Target sample rate
            
        Returns:
            normalized_audio: Normalized audio tensor
        """
        # Convert to tensor if needed
        if not isinstance(audio_data, torch.Tensor):
            if isinstance(audio_data, np.ndarray):
                audio_data = torch.from_numpy(audio_data)
            else:
                audio_data = torch.tensor(audio_data)
        
        # Ensure float32
        if audio_data.dtype != torch.float32:
            audio_data = audio_data.float()
            
        # Normalize to [-1, 1]
        if audio_data.max() > 1.0 or audio_data.min() < -1.0:
            audio_data = audio_data / 32768.0
            
        return audio_data
    
    def _resample_audio(self, audio_data, orig_sr, target_sr=16000):
        """
        Resample audio to target sample rate
        
        Args:
            audio_data: Audio tensor
            orig_sr: Original sample rate
            target_sr: Target sample rate
            
        Returns:
            resampled_audio: Resampled audio tensor
        """
        if orig_sr != target_sr:
            resampler = torchaudio.transforms.Resample(orig_sr, target_sr)
            audio_data = resampler(audio_data)
        return audio_data
    
    def _simple_vad(self, audio_data, sample_rate=16000):
        """
        Simple energy-based voice activity detection
        
        Args:
            audio_data: Audio tensor
            sample_rate: Sample rate
            
        Returns:
            filtered_audio: Audio with only speech segments
        """
        # Convert to numpy if needed
        if isinstance(audio_data, torch.Tensor):
            audio_numpy = audio_data.numpy()
        else:
            audio_numpy = audio_data
            
        # Simple energy-based VAD
        frame_duration = 0.03  # 30ms frames
        frame_samples = int(sample_rate * frame_duration)
        
        speech_frames = []
        for i in range(0, len(audio_numpy), frame_samples):
            frame = audio_numpy[i:i+frame_samples]
            if len(frame) > 0:
                # Calculate energy (RMS)
                energy = np.sqrt(np.mean(frame**2))
                # If energy is above threshold, consider it speech
                if energy > self.vad_energy_threshold:
                    speech_frames.append(frame)
        
        if speech_frames:
            return torch.from_numpy(np.concatenate(speech_frames))
        else:
            return audio_data
    
    def enroll_user(self, user_id, wav_files_list):
        """
        Enroll a user with voice samples
        
        Args:
            user_id (str): User identifier
            wav_files_list (list): List of paths to WAV files
            
        Returns:
            bool: Success status
        """
        try:
            embeddings = []
            
            for wav_file in wav_files_list:
                if not os.path.exists(wav_file):
                    print(f"Warning: File {wav_file} not found")
                    continue
                    
                # Load audio
                signal, sr = torchaudio.load(wav_file)
                signal = signal.squeeze()  # Remove channel dimension if mono
                
                # Process audio
                signal = self._normalize_audio(signal, sr)
                signal = self._resample_audio(signal, sr)
                signal = self._simple_vad(signal)
                
                # Get embedding
                embedding = self.classifier.encode_batch(signal.unsqueeze(0))
                embeddings.append(embedding.squeeze().numpy())
            
            if embeddings:
                # Average embeddings
                avg_embedding = np.mean(embeddings, axis=0)
                self.enrollments[user_id] = avg_embedding
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error enrolling user {user_id}: {e}")
            return False
    
    def verify_speaker(self, user_id, audio_chunk):
        """
        Verify if audio chunk belongs to enrolled user
        
        Args:
            user_id (str): User identifier
            audio_chunk: Audio data (numpy array, tensor, or bytes)
            
        Returns:
            dict: Verification result with accept flag and score
        """
        try:
            # Check if user is enrolled
            if user_id not in self.enrollments:
                return {"accept": False, "score": 0.0}
            
            # Convert audio chunk to tensor
            if isinstance(audio_chunk, bytes):
                # Convert bytes to numpy array
                audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
                audio_tensor = torch.from_numpy(audio_data).float()
                # Normalize
                audio_tensor = audio_tensor / 32768.0
            elif isinstance(audio_chunk, np.ndarray):
                audio_tensor = torch.from_numpy(audio_chunk).float()
                # Normalize if needed
                if audio_tensor.max() > 1.0 or audio_tensor.min() < -1.0:
                    audio_tensor = audio_tensor / 32768.0
            else:
                audio_tensor = audio_chunk.float()
            
            # Process audio
            audio_tensor = self._normalize_audio(audio_tensor)
            audio_tensor = self._simple_vad(audio_tensor)
            
            # Skip if no speech detected
            if len(audio_tensor) < 160:  # Less than 10ms at 16kHz
                return {"accept": False, "score": 0.0}
            
            # Get embedding
            embedding = self.classifier.encode_batch(audio_tensor.unsqueeze(0))
            embedding = embedding.squeeze().numpy()
            
            # Compare with enrolled embedding
            enrolled_embedding = self.enrollments[user_id]
            similarity = cosine_similarity([embedding], [enrolled_embedding])[0][0]
            
            # Return result
            return {
                "accept": similarity >= self.threshold,
                "score": float(similarity)
            }
            
        except Exception as e:
            print(f"Error verifying speaker: {e}")
            return {"accept": False, "score": 0.0}
    
    def set_threshold(self, threshold):
        """
        Set verification threshold
        
        Args:
            threshold (float): New threshold value
        """
        self.threshold = threshold

# Example usage
if __name__ == "__main__":
    # Create verifier
    verifier = SpeakerVerifier()
    
    # Example enrollment (you would provide actual WAV files)
    # verifier.enroll_user("myself", ["enroll1.wav", "enroll2.wav", "enroll3.wav"])
    
    print("Speaker Verifier module ready")