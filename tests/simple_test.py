#!/usr/bin/env python3
"""
Simple test script to verify basic functionality
"""

import os
import sys
from dotenv import dotenv_values

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

print(f"🚀 Starting {Assistantname} AI Assistant Simple Test")
print("=" * 50)

def test_model_import():
    """Test importing the Model module"""
    print("🔧 Testing Model import...")
    try:
        from Backend.Model import FirstLayerDMM
        print("✅ Model module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_chatbot_import():
    """Test importing the Chatbot module"""
    print("🔧 Testing Chatbot import...")
    try:
        from Backend.Chatbot import ChatBot
        print("✅ Chatbot module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Chatbot import failed: {e}")
        return False

def main():
    """Main test function"""
    print(f"👋 Hello {Username}! I'm {Assistantname}, your AI assistant.")
    
    # Test individual imports
    model_success = test_model_import()
    chatbot_success = test_chatbot_import()
    
    if model_success and chatbot_success:
        print(f"\n🎉 {Assistantname} core modules are working correctly!")
    else:
        print(f"\n⚠️  {Assistantname} has some import issues that need fixing.")
    
    print(f"\n💡 Next steps:")
    print(f"   - Update API keys in .env file")
    print(f"   - Fix GUI architecture issues")
    print(f"   - Test full functionality")

if __name__ == "__main__":
    main()