#!/usr/bin/env python3
"""
Script to install voice recognition dependencies for Jasmine AI
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def main():
    print("Installing voice recognition dependencies for Jasmine AI...")
    print("=" * 50)
    
    # List of required packages
    required_packages = [
        "webrtcvad",
        "speechbrain",
        "torch",
        "torchaudio",
        "scikit-learn"
    ]
    
    # Optional packages
    optional_packages = [
        "faster-whisper"  # For local speech-to-text
    ]
    
    print("Installing required packages:")
    success_count = 0
    for package in required_packages:
        print(f"  Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\nRequired packages installation complete: {success_count}/{len(required_packages)}")
    
    print("\nInstalling optional packages (for local STT):")
    optional_success = 0
    for package in optional_packages:
        print(f"  Installing {package}...")
        if install_package(package):
            optional_success += 1
    
    print(f"\nOptional packages installation complete: {optional_success}/{len(optional_packages)}")
    
    print("\n" + "=" * 50)
    if success_count == len(required_packages):
        print("✓ All required packages installed successfully!")
        print("You can now use the voice recognition features.")
    else:
        print("⚠ Some packages failed to install. Check the errors above.")
        print("You may need to install them manually or check your Python environment.")
    
    print("\nTo manually install packages, run:")
    print("pip install webrtcvad speechbrain torch torchaudio scikit-learn")
    print("pip install faster-whisper  # Optional, for local speech-to-text")

if __name__ == "__main__":
    main()