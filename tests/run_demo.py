#!/usr/bin/env python3
"""
Run a demo of the Jarvis AI Assistant core functionality
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

print(f"🚀 Starting {Assistantname} AI Assistant Demo")
print("=" * 50)

def test_basic_functionality():
    """Test that the basic structure works"""
    print("🔧 Testing Basic Functionality...")
    
    # Test imports
    try:
        # Test backend imports
        from Backend.Model import FirstLayerDMM
        from Backend.Chatbot import ChatBot
        from Backend.RealtimeSearchEngine import RealtimeSearchEngine
        from Backend.TextToSpeech import TextToSpeech
        from Backend.ImageGeneration import GenerateImages
        print("✅ All backend modules imported successfully")
        
        # Test frontend imports (GUI might fail due to PyQt5 issues)
        try:
            from Frontend.GUI import QueryModifier
            print("✅ Frontend modules imported successfully")
        except Exception as e:
            print(f"⚠️  Frontend GUI import failed (known issue): {e}")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def show_project_structure():
    """Show the project structure"""
    print("\n📁 Project Structure:")
    print("-" * 20)
    print("Main.py              # Main entry point")
    print("Backend/             # AI and logic components")
    print("  ├── Model.py        # Decision making")
    print("  ├── Chatbot.py      # Conversational AI")
    print("  ├── RealtimeSearchEngine.py  # Web search")
    print("  ├── Automation.py   # System automation")
    print("  ├── SpeechToText.py # Voice recognition")
    print("  ├── TextToSpeech.py # Voice synthesis")
    print("  └── ImageGeneration.py  # Image creation")
    print("Frontend/            # User interface")
    print("  └── GUI.py          # Graphical interface")
    print("Data/                # Storage directory")
    print("Requirements.txt     # Dependencies list")

def show_next_steps():
    """Show what's needed to run the full program"""
    print("\n📋 To Run the Full Program:")
    print("-" * 25)
    print("1. Update API keys in .env file:")
    print("   - CohereAPIKey (for decision making)")
    print("   - GroqAPIKey (for chatbot)")
    print("   - HuggingFaceAPIKey (for image generation)")
    print("\n2. Fix GUI issues:")
    print("   - Migrate from PyQt5 to PyQt6")
    print("   - Command: pip3 install PyQt6")
    print("\n3. Update deprecated models:")
    print("   - Check current model names for Cohere and Groq")
    print("\n4. Run the main program:")
    print("   - python3 Main.py")

def main():
    """Main demo function"""
    print(f"👋 Hello {Username}! I'm {Assistantname}, your AI assistant.")
    
    # Test basic functionality
    if test_basic_functionality():
        print(f"\n🎉 {Assistantname} structure is working correctly!")
    else:
        print(f"\n❌ {Assistantname} has structural issues that need fixing.")
        return
    
    # Show project structure
    show_project_structure()
    
    # Show next steps
    show_next_steps()
    
    print(f"\n💡 Tip: The core structure is solid. To use AI features,")
    print(f"   you'll need to update the API keys and models in the code.")

if __name__ == "__main__":
    main()