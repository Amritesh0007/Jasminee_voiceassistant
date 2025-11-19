#!/usr/bin/env python3
"""
Script to set microphone and assistant status
"""

import os

def set_status():
    """Set microphone and assistant status"""
    temp_dir = os.path.join("Frontend", "Files")
    
    # Create directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    # Set microphone status to True
    mic_file = os.path.join(temp_dir, "Mic.data")
    with open(mic_file, "w") as f:
        f.write("True")
    
    # Set assistant status to True (or a meaningful status)
    status_file = os.path.join(temp_dir, "Status.data")
    with open(status_file, "w") as f:
        f.write("Active")
    
    print("✅ Status updated successfully:")
    print("   Microphone status: True")
    print("   Assistant status: Active")
    
    # Verify the changes
    with open(mic_file, "r") as f:
        mic_status = f.read().strip()
    with open(status_file, "r") as f:
        assistant_status = f.read().strip()
    
    print("\n🔍 Verification:")
    print(f"   Mic.data contains: {mic_status}")
    print(f"   Status.data contains: {assistant_status}")

if __name__ == "__main__":
    set_status()