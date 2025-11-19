#!/usr/bin/env python3
"""
Script to toggle the microphone status for Jarvis AI Assistant
"""

import os

def toggle_microphone():
    """Toggle the microphone status between True and False"""
    temp_dir = os.path.join("Frontend", "Files")
    mic_file = os.path.join(temp_dir, "Mic.data")
    
    # Create directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    # Read current status
    try:
        with open(mic_file, "r") as f:
            current_status = f.read().strip()
    except FileNotFoundError:
        current_status = "False"
    
    # Toggle status
    new_status = "True" if current_status.lower() == "false" else "False"
    
    # Write new status
    with open(mic_file, "w") as f:
        f.write(new_status)
    
    print(f"Microphone status changed from '{current_status}' to '{new_status}'")
    print(f"File location: {mic_file}")
    
    return new_status

def set_microphone_status(status):
    """Set the microphone status to a specific value"""
    temp_dir = os.path.join("Frontend", "Files")
    mic_file = os.path.join(temp_dir, "Mic.data")
    
    # Create directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    # Write status
    with open(mic_file, "w") as f:
        f.write(str(status))
    
    print(f"Microphone status set to '{status}'")
    print(f"File location: {mic_file}")
    
    return status

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Set specific status
        status = sys.argv[1].lower()
        if status in ["true", "false"]:
            set_microphone_status(status.capitalize())
        else:
            print("Usage: python toggle_microphone.py [true|false]")
            print("Or run without arguments to toggle between states")
    else:
        # Toggle status
        toggle_microphone()