#!/usr/bin/env python3
"""
Text interface for Jasmine AI Assistant
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def text_interface():
    """Simple text interface for the assistant"""
    print("🤖 Jasmine AI Assistant - Text Interface")
    print("=" * 40)
    print("Type your queries below. Type 'exit' to quit.")
    print("Examples:")
    print("  - Hello, how are you?")
    print("  - Open notepad")
    print("  - Play some music")
    print("  - What's the weather like?")
    print("  - Write an application for sick leave")
    print("=" * 40)
    
    # Import required modules
    try:
        from Backend.Model import FirstLayerDMM
        from Backend.Chatbot import ChatBot
        from Backend.RealtimeSearchEngine import RealtimeSearchEngine
        from Backend.Automation import Automation
        import asyncio
        
        print("✅ All modules loaded successfully")
        print()
        
    except Exception as e:
        print(f"❌ Error loading modules: {e}")
        return
    
    while True:
        try:
            # Get user input
            query = input("You: ").strip()
            
            # Check for exit command
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Jasmine: Goodbye! Have a great day!")
                break
            
            # Skip empty queries
            if not query:
                continue
            
            # Process the query through the decision-making model
            print("🧠 Processing your query...")
            decision = FirstLayerDMM(query)
            print(f"🔍 Decision: {decision}")
            
            # Handle different types of decisions
            G = any([i for i in decision if i.startswith("general")])
            R = any([i for i in decision if i.startswith("realtime")])
            
            if G and R or R:
                # Real-time search query
                print("🌐 Searching the web for real-time information...")
                answer = RealtimeSearchEngine(query)
                print(f"Jasmine: {answer}")
            elif G:
                # General chat query
                print("💬 Generating response...")
                answer = ChatBot(query)
                print(f"Jasmine: {answer}")
            else:
                # Automation commands
                print("⚙️  Executing automation commands...")
                asyncio.run(Automation(decision))
                print("Jasmine: Command executed!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Jasmine: I'm sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    text_interface()