#!/usr/bin/env python3
"""
Quick test to verify the fixes
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Jarvis AI Assistant - Quick Test")
print("=" * 35)

# Test imports
try:
    from Backend.Model import FirstLayerDMM
    print("✅ Model module: OK")
except Exception as e:
    print(f"❌ Model module: {e}")

try:
    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
    print("✅ RealtimeSearchEngine module: OK")
except Exception as e:
    print(f"❌ RealtimeSearchEngine module: {e}")

try:
    from Backend.Chatbot import ChatBot
    print("✅ Chatbot module: OK")
except Exception as e:
    print(f"❌ Chatbot module: {e}")

print("\n🎉 Quick test completed!")