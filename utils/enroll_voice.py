#!/usr/bin/env python3
"""
Voice enrollment script for Speaker Verification
"""
import sys
import os
import argparse

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.SpeakerVerifier import SpeakerVerifier

def main():
    parser = argparse.ArgumentParser(description="Enroll voice samples for speaker verification")
    parser.add_argument("user_id", help="User identifier (e.g., 'myself')")
    parser.add_argument("wav_files", nargs="+", help="Paths to WAV files for enrollment")
    
    args = parser.parse_args()
    
    # Create verifier
    verifier = SpeakerVerifier()
    
    # Enroll user
    print(f"Enrolling user: {args.user_id}")
    print(f"Using files: {args.wav_files}")
    
    success = verifier.enroll_user(args.user_id, args.wav_files)
    
    if success:
        print(f"✅ Successfully enrolled {args.user_id}")
        print("Speaker verification is now ready for use!")
    else:
        print(f"❌ Failed to enroll {args.user_id}")
        print("Please check that the WAV files exist and are valid.")

if __name__ == "__main__":
    main()