import json  # Ensure the import is used
from json import load, dump
from dotenv import dotenv_values
import requests
import datetime
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backend.GeminiAPI import gemini_api, chat_completion

# Get the correct path to .env file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, '.env')
env_vars = dotenv_values(env_path)

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
You have excellent emotional intelligence and can understand and respond to human emotions appropriately.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
except json.JSONDecodeError:
    print("ChatLog.json is empty or corrupted. Initializing with an empty list.")
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed:\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response """

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Handle special emotional cases with more sophisticated responses
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
        
        is_emotional = any(emotion in Query.lower() for emotion in emotional_queries)
        is_translation_request = any(indicator in Query.lower() for indicator in translation_indicators)
        
        # Only treat as emotional if it's an emotional query and NOT a translation request
        if is_emotional and not is_translation_request:
            # Provide a more sophisticated, emotionally intelligent response
            emotional_prompt = f"""
            The user has expressed romantic feelings toward you. Respond with emotional intelligence, empathy, and respect. 
            Acknowledge their feelings without encouraging unrealistic expectations. Be kind but clear about boundaries.
            User said: {Query}
            """
            
            # Try to use Gemini for emotionally intelligent response
            if gemini_api.model:
                emotional_messages = [
                    {"role": "user", "content": emotional_prompt}
                ]
                emotional_response = chat_completion(emotional_messages, temperature=0.8)
                if emotional_response:
                    Answer = emotional_response
                else:
                    # Fallback response
                    Answer = "I appreciate your sentiment and the connection you feel. As an AI assistant, I'm designed to be a helpful companion for information and tasks. I care about helping you achieve your goals. Is there something specific I can assist you with today?"
            else:
                # Fallback response
                Answer = "I appreciate your sentiment and the connection you feel. As an AI assistant, I'm designed to be a helpful companion for information and tasks. I care about helping you achieve your goals. Is there something specific I can assist you with today?"
        else:
            # Regular query processing with Gemini API
            if gemini_api.model:
                # Prepare conversation history for context-aware responses
                conversation_history = [
                    {"role": "user", "content": System},
                    {"role": "assistant", "content": "Understood. I'm ready to help with emotional intelligence and empathy."}
                ]
                
                # Add recent chat history for context (last 3 exchanges for faster processing)
                recent_chats = messages[-3:] if len(messages) > 3 else messages
                for entry in recent_chats:
                    conversation_history.append({
                        "role": entry["role"], 
                        "content": entry["content"]
                    })
                
                # Add current query with emotional context awareness
                conversation_history.append({
                    "role": "user", 
                    "content": f"Consider emotional context in your response: {Query}"
                })
                
                # Get response from Gemini with optimized parameters for speed
                Answer = chat_completion(conversation_history, temperature=0.5, max_tokens=512)
                
                # Fallback to basic response if Gemini fails
                if not Answer:
                    Answer = f"I understand you're asking about {Query}. As an AI, I'm here to help with information and tasks while being empathetic to your needs."
            else:
                # Original Groq fallback (if configured)
                messages.append({"role": "user", "content": f"{Query}"})
                
                try:
                    from groq import Groq
                    client = Groq(api_key=GroqAPIKey)
                    
                    SystemChatBot = [
                        {"role": "system", "content": System}
                    ]
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
                        max_tokens=1024,
                        temperature=0.7,
                        top_p=1,
                        stream=True,
                        stop=None
                    )

                    Answer = ""

                    for chunk in completion:
                        if chunk.choices[0].delta.content:
                            Answer += chunk.choices[0].delta.content

                    Answer = Answer.replace("</s>", "")
                except Exception as e:
                    # Final fallback
                    Answer = f"I understand you're asking about {Query}. As an AI, I'm here to help with information and tasks while being empathetic to your needs."

        # Save conversation to chat log
        messages.append({"role": "user", "content": Query})
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return Answer  # Return the answer to the main function

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "Connection error, please try again."
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "An error occurred, please try again."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        response = ChatBot(user_input)
        print(response)  # Print the response to the user