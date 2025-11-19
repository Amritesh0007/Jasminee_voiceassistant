import pygame
import random
import asyncio
import requests
import os
import json
import time
from dotenv import dotenv_values

# Load environment variables with absolute path
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)

Assistantname = env_vars.get("Assistantname")
MurfAPIKey = env_vars.get("MurfAPIKey")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) -> None:
    file_path = os.path.join("Data", "speech.wav")  # Change to .wav extension

    if os.path.exists(file_path):
        os.remove(file_path)

    # Use Murf API for text-to-speech
    if MurfAPIKey:
        # Try Murf API with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Murf API endpoint for text-to-speech
                url = "https://api.murf.ai/v1/speech/generate"
                
                # Use the api-key header format
                headers = {
                    "api-key": MurfAPIKey,
                    "Content-Type": "application/json"
                }
                
                # Request payload with a valid voice ID from the Murf API
                # Add speech rate control to make it slower as per user preference
                payload = {
                    "text": text,
                    "voiceId": "en-US-alina",  # Use a valid voice ID from the API
                    "audioFormat": "wav",  # Request WAV format directly
                    "rate": "-20%"  # Slow down speech by 20% for better clarity
                }
                
                # Make the API request with shorter timeout for faster fallback
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                # If WAV format is not supported, try with speed parameter
                if response.status_code != 200:
                    payload = {
                        "text": text,
                        "voiceId": "en-US-alina",
                        "audioFormat": "mp3",
                        "speed": "slow",
                        "rate": "-20%"  # Slow down speech by 20% for better clarity
                    }
                    response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                # If speed parameter is not supported either, try without rate control
                if response.status_code != 200:
                    payload = {
                        "text": text,
                        "voiceId": "en-US-alina",
                        "audioFormat": "mp3"
                    }
                    response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    # Parse the JSON response to get the audio URL
                    response_data = response.json()
                    if 'audioFile' in response_data:
                        # Download the actual audio file
                        audio_response = requests.get(response_data['audioFile'], timeout=15)
                        if audio_response.status_code == 200:
                            # Save the audio file
                            with open(file_path, "wb") as f:
                                f.write(audio_response.content)
                            print("Audio generated successfully using Murf API")
                            
                            # Verify the file is valid by checking its size
                            if os.path.getsize(file_path) > 0:
                                return
                            else:
                                print("Murf API generated empty audio file, falling back to Edge TTS")
                                os.remove(file_path)  # Remove the empty file
                        else:
                            print(f"Failed to download audio file: {audio_response.status_code}")
                    else:
                        print("Murf API response doesn't contain audioFile")
                else:
                    print(f"Murf API error: {response.status_code} - {response.text}")
                    
                    # If this is not the last attempt, wait before retrying
                    if attempt < max_retries - 1:
                        print(f"Retrying Murf API (attempt {attempt + 2}/{max_retries})...")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    
            except Exception as e:
                print(f"Error using Murf API (attempt {attempt + 1}/{max_retries}): {e}")
                
                # If this is not the last attempt, wait before retrying
                if attempt < max_retries - 1:
                    print(f"Retrying Murf API (attempt {attempt + 2}/{max_retries})...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
        
        # Fallback to Edge TTS if Murf fails after all retries
        print("Falling back to Edge TTS after Murf API failures")
        await fallbackToEdgeTTS(text)
    else:
        # Fallback to Edge TTS if no Murf API key
        await fallbackToEdgeTTS(text)

async def fallbackToEdgeTTS(text):
    """Fallback to Edge TTS if Murf API is not available or fails"""
    try:
        import edge_tts
        # Ensure we have a valid voice
        voice = AssistantVoice if AssistantVoice else "en-US-JennyNeural"
        # Set a slower speech rate as per user preference
        communicate = edge_tts.Communicate(text, voice, pitch='+5Hz', rate='-20%')
        file_path = os.path.join("Data", "speech.wav")  # Keep .wav extension
        await communicate.save(file_path)
        print("Audio generated using Edge TTS (fallback)")
    except ImportError:
        print("Edge TTS not available. Please install edge-tts: pip install edge-tts")
        # Create a simple beep sound as fallback
        pygame.mixer.init()
        # This would be a more complex fallback in a real implementation
    except Exception as e:
        print(f"Error in Edge TTS: {e}")

def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))

            file_path = os.path.join("Data", "speech.wav")  # Keep .wav extension
            print(f"Attempting to play audio file: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            if os.path.exists(file_path):
                print(f"File size: {os.path.getsize(file_path)} bytes")
            
            # Check if file exists and is not empty
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                # Try to play using system default player
                import platform
                import subprocess
                
                system = platform.system().lower()
                try:
                    if system == "darwin":  # macOS
                        subprocess.run(["afplay", file_path], check=True, timeout=30)
                    elif system == "windows":
                        subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"], 
                                     check=True, timeout=30)
                    else:  # Linux and others
                        subprocess.run(["paplay", file_path], check=True, timeout=30)
                    
                    print("Audio played successfully using system player")
                    # Add a normal pause after playing
                    time.sleep(0.3)
                    return True
                except Exception as system_play_error:
                    print(f"System player failed: {system_play_error}")
                    # Fallback to pygame
                    print("Initializing pygame mixer...")
                    # Force initialization of pygame mixer
                    pygame.mixer.quit()  # Clean up any previous instances
                    pygame.mixer.init()
                    
                    print("Loading audio file...")
                    # Load and play audio
                    pygame.mixer.music.load(file_path)
                    print("Playing audio...")
                    pygame.mixer.music.play()
                    
                    # Wait for playback to complete
                    clock = pygame.time.Clock()
                    playback_start = time.time()
                    while pygame.mixer.music.get_busy():
                        pygame.mixer.music.set_volume(1.0)  # Ensure volume is at maximum
                        clock.tick(10)
                        # Timeout after 30 seconds to prevent infinite loops
                        if time.time() - playback_start > 30:
                            print("Audio playback timeout")
                            break
                    
                    print("Audio playback completed")
                    # Add a normal pause after playing
                    time.sleep(0.3)
                    
                    # Clean up
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    
                    print("Audio played successfully")
                    return True
            else:
                print("No valid audio file found")
                return False
        except Exception as e:
            print(f"Error in TTS: {e}")
            import traceback
            traceback.print_exc()
            return False

def TextToSpeech(Text, func=lambda r=None: True):
    # Apply text processing to make speech clearer and slower
    # Add slight pauses by adding commas where appropriate
    sentence_count = Text.count('. ')
    processed_text = Text.replace('. ', '. , ', sentence_count // 2)  # Add pauses to every other sentence
    
    Data = str(processed_text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # Check if this is an emotional response that should be spoken as a whole
    emotional_indicators = [
        "I understand you're feeling",
        "I'm sorry to hear that",
        "I appreciate you sharing",
        "It sounds like you're going through",
        "I can sense that you're",
        "Thank you for trusting me"
    ]
    
    is_emotional_response = any(indicator in Text for indicator in emotional_indicators)
    
    # For long texts, break them into smaller chunks with normal pauses
    if len(Text) > 250 and not is_emotional_response:  # Only chunk very long texts, but not emotional responses
        # Break into reasonable segments at sentence boundaries
        sentences = Text.split('. ')
        current_chunk = ""
        chunk_word_count = 0
        max_chunk_words = 30  # Maximum words per chunk for natural speech
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                sentence_word_count = len(sentence.split())
                
                # If adding this sentence would exceed the chunk size, or if it's a good breaking point
                if chunk_word_count + sentence_word_count > max_chunk_words and current_chunk:
                    # Play current chunk
                    if current_chunk.strip():
                        TTS(current_chunk, func)
                        # Add a natural pause between chunks
                        time.sleep(0.7)  # Longer pause for sentence boundaries
                    
                    # Start new chunk with current sentence
                    current_chunk = sentence + ("." if not sentence.endswith(".") else "")
                    chunk_word_count = sentence_word_count
                else:
                    # Add sentence to current chunk
                    if current_chunk:
                        current_chunk += ". " + sentence
                    else:
                        current_chunk = sentence + ("." if not sentence.endswith(".") else "")
                    chunk_word_count += sentence_word_count
        
        # Play the last chunk
        if current_chunk.strip():
            TTS(current_chunk, func)
            time.sleep(0.5)
                
        # For long texts, also add the response
        if len(Data) > 4:
            TTS(random.choice(responses), func)
            time.sleep(0.3)
    else:
        # For shorter texts or emotional responses, play normally as a single unit
        TTS(Text, func)
        if len(Text) < 30:
            time.sleep(0.3)  # Short pause at the end for short responses

# jar tumhala purna read karaich lavaich asel tr TTS cha use kara jar 4 or tya peksha line 
# jast lines text asel tr TTS use kra ani Short made read karacih asel tr texttosppech use kara  
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text : "))