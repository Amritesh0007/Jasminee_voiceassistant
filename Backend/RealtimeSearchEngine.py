from googlesearch import search
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backend.GeminiAPI import gemini_api, chat_completion

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Ensure Data directory exists
data_dir = "Data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

try:
    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
except FileNotFoundError:
    # Create the file with an empty list if it doesn't exist
    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump([], f)
    messages = []
except JSONDecodeError:
    print("ChatLog.json is empty or corrupted. Initializing with an empty list.")
    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump([], f)
    messages = []

def GoogleSearch(query):
    try:
        # Try advanced search first
        results = list(search(query, advanced=True, num_results=5))
        
        # If advanced search returns no results, try simple search
        if not results:
            results = list(search(query, num_results=5))
            
        if results:
            Answer = f"The search results for '{query}' are :\n[start]\n"

            for i in results:
                # Convert to string to avoid attribute access issues
                result_str = str(i)
                Answer += f"Result: {result_str}\n\n"

            Answer += "[end]"
            return Answer
        else:
            # Return a fallback message if no results found
            return f"No search results found for '{query}'.\n[start]\nNo search results available.\n[end]"
    except Exception as e:
        # Return a fallback message if search fails
        return f"Unable to perform search for '{query}'. Error: {str(e)}\n[start]\nNo search results available.\n[end]"

def get_weather_info(location):
    """Get weather information for a specific location using Open-Meteo API"""
    try:
        # List of location variations to try
        location_variations = [location]
        
        # Add common variations for better matching
        location_lower = location.lower()
        if ' ' in location_lower:
            # For multi-word locations, also try without spaces or with underscores
            location_variations.append(location_lower.replace(' ', ''))
            location_variations.append(location_lower.replace(' ', '_'))
        
        # Add common alternative names for Indian states
        state_alternatives = {
            'andhra pradesh': ['Amaravati', 'Visakhapatnam', 'Andhra'],
            'tamil nadu': ['Chennai', 'Madras', 'Tamil'],
            'uttar pradesh': ['Lucknow', 'Kanpur', 'Uttar'],
            'madhya pradesh': ['Bhopal', 'Indore', 'Madhya'],
        }
        
        # Add alternatives if available
        alternatives_to_add = []
        for key, alternatives in state_alternatives.items():
            if key in location_lower:
                alternatives_to_add.extend(alternatives)
        location_variations.extend(alternatives_to_add)
        
        # Try each location variation with a timeout
        geo_data = None
        resolved_location = None
        lat = None
        lon = None
        
        for loc in location_variations:
            try:
                # First, we need to get the coordinates for the location
                geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={loc}&count=1&language=en&format=json"
                geo_response = requests.get(geocoding_url, timeout=5)
                geo_data = geo_response.json()
                
                if 'results' in geo_data and geo_data['results']:
                    # Get coordinates
                    lat = geo_data['results'][0]['latitude']
                    lon = geo_data['results'][0]['longitude']
                    resolved_location = geo_data['results'][0]['name']
                    break
            except Exception:
                # Continue to next variation if this one fails
                continue
        
        if not resolved_location:
            return f"Sorry, I couldn't find weather information for {location}."
        
        # Get current weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()
        
        if 'current_weather' not in weather_data:
            return f"Sorry, I couldn't retrieve weather data for {resolved_location}."
        
        # Extract weather information
        current = weather_data['current_weather']
        temperature = current['temperature']
        windspeed = current['windspeed']
        weather_code = current['weathercode']
        
        # Simple weather code interpretation
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snow fall",
            73: "moderate snow fall",
            75: "heavy snow fall",
            95: "thunderstorm",
        }
        
        weather_description = weather_descriptions.get(weather_code, "unknown weather condition")
        
        return f"The current weather in {resolved_location} is {temperature}°C with {weather_description} and wind speed of {windspeed} km/h."
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve weather information for {location}. Error: {str(e)}"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# SystemChatBot is no longer needed since we're using Gemini API exclusively
# SystemChatBot = [
#     {"role": "system", "content": System},
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello, Sir, how can I help you?"}
# ]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

def RealtimeSearchEngine(prompt):
    global messages
    
    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Check if this is a weather query
    weather_keywords = ["weather", "temperature", "forecast", "climate", "rain", "snow", "sunny", "cloudy", "windy", "hot", "cold"]
    is_weather_query = any(keyword in prompt.lower() for keyword in weather_keywords)
    
    if is_weather_query:
        # Extract location from the prompt with improved logic
        location = ""
        
        # Clean the prompt - remove parentheses and extra formatting
        clean_prompt = prompt.lower()
        clean_prompt = clean_prompt.replace("(", "").replace(")", "").strip()
        
        # Handle queries that start with the assistant name
        if clean_prompt.startswith("jasmine "):
            clean_prompt = clean_prompt[8:]  # Remove "jasmine " from the beginning
        
        # Improved location extraction for common patterns
        # Pattern 1: "temperature in [location]"
        if "temperature in " in clean_prompt:
            location = clean_prompt.split("temperature in ", 1)[1].strip()
        # Pattern 2: "weather in [location]"  
        elif "weather in " in clean_prompt:
            location = clean_prompt.split("weather in ", 1)[1].strip()
        # Pattern 3: "how is the temperature in [location]"
        elif "how is the temperature in " in clean_prompt:
            location = clean_prompt.split("how is the temperature in ", 1)[1].strip()
        # Pattern 4: "what is the weather like in [location]"
        elif "what is the weather like in " in clean_prompt:
            location = clean_prompt.split("what is the weather like in ", 1)[1].strip()
        # Pattern 5: General "in [location]" pattern
        elif " in " in clean_prompt:
            location_part = clean_prompt.split(" in ", 1)[1].strip("?").strip(".")
            # Remove common trailing words that are not part of location
            location_words = location_part.split()
            common_trailing_words = ["today", "now", "currently", "please", "thanks", "thank"]
            # Remove trailing words one by one
            while location_words and location_words[-1].lower() in common_trailing_words:
                location_words = location_words[:-1]
            location = " ".join(location_words) if location_words else location_part
        elif " at " in clean_prompt:
            location_part = clean_prompt.split(" at ", 1)[1].strip("?").strip(".")
            # Remove common trailing words that are not part of location
            location_words = location_part.split()
            common_trailing_words = ["today", "now", "currently", "please", "thanks", "thank"]
            # Remove trailing words one by one
            while location_words and location_words[-1].lower() in common_trailing_words:
                location_words = location_words[:-1]
            location = " ".join(location_words) if location_words else location_part
        else:
            # Try to find location after weather-related keywords
            for keyword in weather_keywords:
                if keyword in clean_prompt:
                    parts = clean_prompt.split(keyword, 1)
                    if len(parts) > 1:
                        # Look for the location after the keyword
                        after_keyword = parts[1].strip()
                        if " in " in after_keyword:
                            location_part = after_keyword.split(" in ", 1)[1].strip("?").strip(".")
                            # Remove common trailing words that are not part of location
                            location_words = location_part.split()
                            common_trailing_words = ["today", "now", "currently", "please", "thanks", "thank"]
                            # Remove trailing words one by one
                            while location_words and location_words[-1].lower() in common_trailing_words:
                                location_words = location_words[:-1]
                            location = " ".join(location_words) if location_words else location_part
                            break
                        elif " at " in after_keyword:
                            location_part = after_keyword.split(" at ", 1)[1].strip("?").strip(".")
                            # Remove common trailing words that are not part of location
                            location_words = location_part.split()
                            common_trailing_words = ["today", "now", "currently", "please", "thanks", "thank"]
                            # Remove trailing words one by one
                            while location_words and location_words[-1].lower() in common_trailing_words:
                                location_words = location_words[:-1]
                            location = " ".join(location_words) if location_words else location_part
                            break
        
        # Special handling for common Indian states
        indian_states = [
            "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", 
            "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", 
            "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", 
            "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", 
            "uttar pradesh", "uttarakhand", "west bengal"
        ]
        
        # If location is not found or is too short, try to match with Indian states
        if not location or len(location) < 2:
            for state in indian_states:
                if state in clean_prompt:
                    location = state
                    break
        
        # Clean up the location string
        if location:
            # Remove trailing punctuation and common words
            location = location.strip().strip("?").strip(".").strip()
            # Remove common trailing words
            words = location.split()
            if words and words[-1].lower() in ["today", "now", "currently"]:
                location = " ".join(words[:-1])
        
        print(f"DEBUG: Extracted location for weather query: '{location}' from prompt: '{prompt}'")
        
        if location:
            # Get weather information directly
            weather_info = get_weather_info(location)
            Answer = weather_info
        else:
            # Fall back to search if we can't determine location
            search_results = GoogleSearch(prompt)
            Answer = f"I found the following search results for '{prompt}': {search_results}"
    else:
        # Regular search for non-weather queries
        search_results = GoogleSearch(prompt)
        
        # Use Gemini API for processing search results
        if gemini_api.model:
            # Prepare conversation history for context-aware responses
            conversation_history = [
                {"role": "user", "content": System},
                {"role": "assistant", "content": "Understood. I'm ready to help with search results."}
            ]
            
            # Add recent chat history for context (last 3 exchanges for faster processing)
            recent_chats = messages[-3:] if len(messages) > 3 else messages
            for entry in recent_chats:
                conversation_history.append({
                    "role": entry["role"], 
                    "content": entry["content"]
                })
            
            # Check if search results are available
            if "No search results available" not in search_results:
                # Add search results and current query
                conversation_history.append({
                    "role": "user", 
                    "content": f"Here are the search results for '{prompt}': {search_results}"
                })
                conversation_history.append({
                    "role": "user", 
                    "content": f"Use the search results to provide an accurate answer to: {prompt}. Include real-time information if needed: {Information()}"
                })
            else:
                # No search results, ask Gemini to provide general knowledge
                conversation_history.append({
                    "role": "user", 
                    "content": f"No search results were found for '{prompt}'. Please provide an answer based on your general knowledge. Include real-time information if needed: {Information()}"
                })
            
            # Get response from Gemini with optimized parameters for speed
            Answer = chat_completion(conversation_history, temperature=0.5, max_tokens=512)
            
            # Fallback if Gemini fails
            if not Answer:
                Answer = f"I found the following search results for '{prompt}': {search_results}"
        else:
            # If Gemini is not available, return search results directly
            Answer = f"I found the following search results for '{prompt}': {search_results}"

    messages.append({"role": "assistant", "content": Answer})

    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query: ")
        print(RealtimeSearchEngine(prompt))