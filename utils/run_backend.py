#!/usr/bin/env python3
"""
Run the backend components of Jarvis AI Assistant without GUI
"""

import os
import sys
import json
from dotenv import dotenv_values
from time import sleep

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

print(f"Initializing {Assistantname} AI Assistant...")
print(f"Welcome {Username}!")
print("=" * 50)

# Import backend components
try:
    from Backend.Model import FirstLayerDMM
    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
    from Backend.Chatbot import ChatBot
    from Backend.TextToSpeech import TextToSpeech
    print("✅ Backend modules loaded successfully")
except Exception as e:
    print(f"❌ Failed to load backend modules: {e}")
    sys.exit(1)

def setup_data_files():
    """Ensure required data files exist"""
    # Create Data directory if it doesn't exist
    if not os.path.exists("Data"):
        os.makedirs("Data")
        print("📁 Created Data directory")
    
    # Create ChatLog.json if it doesn't exist
    chatlog_path = os.path.join("Data", "ChatLog.json")
    if not os.path.exists(chatlog_path):
        with open(chatlog_path, "w") as f:
            json.dump([], f)
        print("📄 Created ChatLog.json")
    
    # Create Frontend/Files directory if it doesn't exist
    frontend_files_path = os.path.join("Frontend", "Files")
    if not os.path.exists(frontend_files_path):
        os.makedirs(frontend_files_path)
        print("📁 Created Frontend/Files directory")
    
    # Create required status files
    status_files = ["Mic.data", "Status.data", "Responses.data", "Database.data"]
    for file_name in status_files:
        file_path = os.path.join(frontend_files_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("")
            print(f"📄 Created {file_name}")

def query_modifier(query):
    """Simple query modifier for testing"""
    new_query = query.lower().strip()
    query_words = new_query.split()
    question_words = ['how','what','who','where','when','why','which','whom','can you',"what's", "where's","how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += '.'

    return new_query.capitalize()

def main():
    """Main execution loop for backend testing"""
    print("\n🤖 Jarvis AI Assistant Backend Test")
    print("=" * 40)
    print("Type 'exit' to quit")
    print("Type 'test' for a sample query")
    print("-" * 40)
    
    while True:
        try:
            # Get user input
            user_input = input(f"\n{Username}: ").strip()
            
            if user_input.lower() == 'exit':
                print(f"\n{Assistantname}: Goodbye!")
                break
            
            if user_input.lower() == 'test':
                user_input = "Hello, how are you today?"
                print(f"{Username}: {user_input}")
            
            if not user_input:
                continue
            
            # Process the query through the decision making model
            print(f"\n{Assistantname}: Processing your query...")
            decision = FirstLayerDMM(user_input)
            print(f"Decision: {decision}")
            
            # Handle different types of queries
            if any("general" in d for d in decision):
                # Handle general queries with chatbot
                print(f"{Assistantname}: Thinking...")
                answer = ChatBot(user_input)
                print(f"{Assistantname}: {answer}")
                
            elif any("realtime" in d for d in decision):
                # Handle realtime queries with search engine
                print(f"{Assistantname}: Searching...")
                answer = RealtimeSearchEngine(user_input)
                print(f"{Assistantname}: {answer}")
                
            elif any("exit" in d for d in decision):
                print(f"{Assistantname}: Goodbye!")
                break
                
            else:
                # Default to chatbot for other queries
                print(f"{Assistantname}: Responding...")
                answer = ChatBot(user_input)
                print(f"{Assistantname}: {answer}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Assistantname}: Goodbye!")
            break
        except Exception as e:
            print(f"\n{Assistantname}: Sorry, I encountered an error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    # Setup required files
    setup_data_files()
    
    # Run the main loop
    main()