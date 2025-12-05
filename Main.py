from Frontend.GUI import (
    GraphicalUserInterface,
    SetAsssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.GeminiAPI import gemini_api, generate_text, solve_math_problem


try:
    import utils.fix_torchaudio
    utils.fix_torchaudio.patch_torchaudio()
except ImportError:
    print("Warning: Could not apply torchaudio patch")

from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables with absolute path
env_path = os.path.join(os.path.dirname(__file__), ".env")
env_vars = dotenv_values(env_path)
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# Ensure Data directory exists
data_dir = "Data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

DefaultMessage = f""" {Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you? """

functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
subprocess_list = []



# Ensure a default chat log exists if no chats are logged
def ShowDefaultChatIfNoChats():
    try:
        with open('Data/ChatLog.json', "r", encoding='utf-8') as file:
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as temp_file:
                    temp_file.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
                    response_file.write(DefaultMessage)
    except FileNotFoundError:
        print("ChatLog.json file not found. Creating default response.")
        os.makedirs("Data", exist_ok=True)
        with open('Data/ChatLog.json', "w", encoding='utf-8') as file:
            file.write("[]")
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
            response_file.write(DefaultMessage)

# Read chat log from JSON
def ReadChatLogJson():
    try:
        with open('Data/ChatLog.json', 'r', encoding='utf-8') as file:
            chatlog_data = json.load(file)
        return chatlog_data
    except FileNotFoundError:
        print("ChatLog.json not found.")
        return []

# Integrate chat logs into a readable format


def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    # Ensure the Temp directory exists
    temp_dir_path = TempDirectoryPath('')  # Get the directory path
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

# Display the chat on the GUI
def ShowChatOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
            data = file.read()
        if len(str(data)) > 0:
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
                response_file.write(data)
    except FileNotFoundError:
        print("Database.data file not found.")

# Initial execution setup
def InitialExecution():
    SetMicrophoneStatus("True")  # Set microphone status to True by default
    SetAsssistantStatus("Active")  # Set assistant status to Active by default
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatOnGUI()

# Main execution logic
def MainExecution():
    try:
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAsssistantStatus("Listening...")
        Query = SpeechRecognition()
        ShowTextToScreen(f"{Username}: {Query}")
        SetAsssistantStatus("Thinking...")
        Decision = FirstLayerDMM(Query)

        print(f"\nDecision: {Decision}\n")

        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])


        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        for queries in Decision:
            if not TaskExecution:
                if any(queries.startswith(func) for func in functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True

        if ImageExecution:
            with open('Frontend/Files/ImageGeneration.data', "w") as file:
                file.write(f"{ImageGenerationQuery},True")

            try:
                p1 = subprocess.Popen(
                    ['python', "Backend/ImageGeneration.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=False,
                )
                subprocess_list.append(p1)
            except Exception as e:
                print(f"Error starting ImageGeneration.py: {e}")

        if G and R or R:
            SetAsssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAsssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
        else:
            for queries in Decision:
                if "mathematics" in queries:
                    # Handle mathematical queries
                    SetAsssistantStatus("Calculating...")
                    try:
                        from Backend.Mathematics import process_mathematical_query
                        QueryFinal = queries.replace("mathematics", "").strip()
                        
                        # Try Gemini API for complex math first with direct answer
                        if gemini_api.model:
                            Answer = solve_math_problem(QueryFinal, direct_answer=True)
                            if Answer:
                                ShowTextToScreen(f"{Assistantname}: {Answer}")
                                SetAsssistantStatus("Answering...")
                                TextToSpeech(Answer)
                                return True
                        
                        # Fallback to existing math processor with direct answer
                        Answer = process_mathematical_query(QueryFinal, direct_answer=True)
                        ShowTextToScreen(f"{Assistantname}: {Answer}")
                        SetAsssistantStatus("Answering...")
                        TextToSpeech(Answer)
                        return True
                    except Exception as e:
                        Answer = f"Sorry, I encountered an error while processing your mathematical query: {str(e)}"
                        ShowTextToScreen(f"{Assistantname}: {Answer}")
                        SetAsssistantStatus("Answering...")
                        TextToSpeech(Answer)
                        return True
                elif "general" in queries:
                    SetAsssistantStatus("Thinking...")
                    QueryFinal = queries.replace("general", "")
                    
                    # Handle special emotional cases with predefined responses
                    # Be more specific to avoid triggering on translation requests
                    emotional_queries = [
                        "im in love with you", 
                        "i love you", 
                        "you can't reject me",
                        "marry me",
                        "will you be my girlfriend",
                        "will you be my boyfriend"
                    ]
                    
                    # Check if the query contains emotional content but not translation requests
                    # Translation requests typically contain words like 'translate', 'language', 'french', etc.
                    translation_indicators = [
                        "translate", "translation", "language", "french", "spanish", "german", 
                        "italian", "portuguese", "russian", "chinese", "japanese", "korean",
                        "hindi", "arabic", "urdu", "bengali", "punjabi", "tamil", "telugu",
                        "marathi", "gujarati", "kannada", "malayalam", "sinhala", "thai",
                        "vietnamese", "indonesian", "malay", "filipino", "burmese", "khmer"
                    ]
                    
                    is_emotional = any(emotion in QueryFinal.lower() for emotion in emotional_queries)
                    is_translation_request = any(indicator in QueryFinal.lower() for indicator in translation_indicators)
                    
                    # Only treat as emotional if it's an emotional query and NOT a translation request
                    if is_emotional and not is_translation_request:
                        # Provide a polite, predefined response
                        Answer = "I appreciate your sentiment, but as an AI assistant, I don't have personal feelings or relationships. I'm here to help you with information and tasks. How else can I assist you today?"
                    else:
                        # Try Gemini API for enhanced responses
                        if gemini_api.model:
                            # Create conversation history for context-aware responses
                            conversation_history = [
                                {"role": "user", "content": f"You are {Assistantname}, a helpful AI assistant. Respond naturally and concisely."},
                                {"role": "assistant", "content": "Understood. I'm ready to help!"}
                            ]
                            
                            # Add recent chat history for context (last 2 exchanges for faster processing)
                            try:
                                with open('Data/ChatLog.json', 'r', encoding='utf-8') as file:
                                    import json
                                    chatlog_data = json.load(file)
                                    # Get last 2 exchanges for faster processing
                                    recent_chats = chatlog_data[-2:] if len(chatlog_data) > 2 else chatlog_data
                                    for entry in recent_chats:
                                        conversation_history.append({
                                            "role": entry["role"], 
                                            "content": entry["content"]
                                        })
                            except Exception as e:
                                print(f"Could not load chat history: {e}")
                            
                            # Add current query
                            conversation_history.append({"role": "user", "content": QueryFinal})
                            
                            # Get response from Gemini with optimized parameters
                            gemini_response = gemini_api.chat_completion(conversation_history, temperature=0.5, max_tokens=512)
                            if gemini_response:
                                Answer = gemini_response
                            else:
                                Answer = ChatBot(QueryModifier(QueryFinal))
                        else:
                            Answer = ChatBot(QueryModifier(QueryFinal))
                    
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                elif "realtime" in queries:
                    SetAsssistantStatus("Searching...")
                    QueryFinal = queries.replace("realtime", "")
                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                elif "exit" in queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    os._exit(1)

    except Exception as e:
        print(f"Error in MainExecution: {e}")

# Thread for primary execution loop
def FirstThread():
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            print(f"Current Microphone Status: {CurrentStatus}")  # Debugging

            if CurrentStatus.lower() == "true":  # Case-insensitive comparison
                print("Executing MainExecution")  # Debugging
                try:
                    MainExecution()
                    # Reset error counter on successful execution
                    consecutive_errors = 0
                except Exception as e:
                    consecutive_errors += 1
                    print(f"Error in MainExecution: {e}")
                    if consecutive_errors >= max_consecutive_errors:
                        print(f"Too many consecutive errors ({consecutive_errors}). Setting microphone status to False to prevent infinite loop.")
                        SetMicrophoneStatus("False")
                        consecutive_errors = 0
            elif CurrentStatus.lower() == "false":
                AIStatus = GetAssistantStatus()
                print(f"Current Assistant Status: {AIStatus}")  # Debugging

                if "Available..." in AIStatus:
                    sleep(0.1)
                else:
                    print("Setting Assistant Status to 'Available...'")  # Debugging
                    SetAsssistantStatus("Available...")
            else:
                print("Unexpected Microphone Status value. Defaulting to 'False'.")  # Debugging
                SetMicrophoneStatus("False")  # Set to False to prevent infinite loop
        except Exception as e:
            print(f"Error in FirstThread: {e}")
            sleep(1)  # Avoid infinite rapid errors



# Thread for GUI execution
def SecondThread():
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"Error in SecondThread: {e}")

# Entry point
if __name__ == "__main__":
    InitialExecution()
   
    thread1 = threading.Thread(target=FirstThread, daemon=True)
    thread1.start()
    SecondThread()