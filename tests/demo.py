#!/usr/bin/env python3
"""
Demo script to showcase Jarvis AI Assistant backend functionality
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

# Import backend components
try:
    from Backend.Model import FirstLayerDMM
    from Backend.Chatbot import ChatBot
    print("✅ Core modules loaded successfully")
except Exception as e:
    print(f"❌ Failed to load modules: {e}")
    sys.exit(1)

def demo_conversation():
    """Demonstrate a simple conversation"""
    print(f"\n👋 Hello {Username}! I'm {Assistantname}, your AI assistant.")
    print("\n🎯 Demo Features:")
    print("1. Decision Making Model")
    print("2. Conversational AI")
    print("\n" + "-" * 50)
    
    # Sample queries to demonstrate functionality
    sample_queries = [
        "Hello, how are you today?",
        "What is artificial intelligence?",
        "Can you tell me a joke?"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n📝 Sample Query {i}: '{query}'")
        
        # Process with Decision Making Model
        print(f"🧠 {Assistantname} is analyzing...")
        try:
            decision = FirstLayerDMM(query)
            print(f"📋 Decision: {decision}")
        except Exception as e:
            print(f"❌ Decision Making Model error: {e}")
            continue
        
        # Get response from Chatbot
        print(f"💬 {Assistantname} is responding...")
        try:
            response = ChatBot(query)
            print(f"🤖 {Assistantname}: {response}")
        except Exception as e:
            print(f"❌ Chatbot error: {e}")
            continue
            
        print("-" * 30)
    
    print(f"\n✨ Demo completed! {Assistantname} is ready to assist you.")

if __name__ == "__main__":
    demo_conversation()