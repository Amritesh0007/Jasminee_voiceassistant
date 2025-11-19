import cohere
from rich import print
from dotenv import dotenv_values
import os

# Load environment variables with absolute path
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)
# Fix: Use the correct environment variable name "CohereAPIKey" and handle whitespace
CohereAPIKey = env_vars.get("CohereAPIKey")

# Check if API key is available and clean it up
if not CohereAPIKey:
    print("Warning: CohereAPIKey not found in .env file")
    CohereAPIKey = None
else:
    # Remove any surrounding whitespace and quotes
    CohereAPIKey = CohereAPIKey.strip().strip('"').strip("'")

# Initialize Cohere client only if API key is available
co = cohere.Client(api_key=CohereAPIKey) if CohereAPIKey else None

funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder", "mathematics"
]

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to simply open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on. Do NOT use this for complex commands that involve searching or playing content within an application.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on. Also use this for commands like 'play humnava music on spotify' - respond with 'play humnava music' and let the system handle playing it on the specified platform.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google, especially for commands like 'search python on chrome' or 'search machine learning on google'. For these commands, respond with 'google search python' or 'google search machine learning' respectively - extract the search query and respond with the google search command.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube, especially for commands like 'search tutorials on youtube' or 'find music videos on youtube'. For these commands, respond with 'youtube search tutorials' or 'youtube search music videos' respectively.
-> Respond with 'mathematics (query)' if a query is asking for mathematical operations like integration, differentiation, solving equations, limits, series, or any calculus and higher-order mathematics operations. For example, if the query is 'integrate x squared', respond with 'mathematics integrate x squared', if the query is 'what is the derivative of sin x', respond with 'mathematics what is the derivative of sin x', if the query is 'solve x^2 + 5x + 6 = 0', respond with 'mathematics solve x^2 + 5x + 6 = 0'.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
*** CRITICAL: For complex commands that involve both opening an application and performing an action within it (like 'search python on chrome' or 'play humnava music on spotify'), respond with the appropriate action command (google search/play) rather than just the open command. The system will handle opening the appropriate application if needed. ***
"""

def FirstLayerDMM(prompt: str = "test"):
    # Check if Cohere client is available
    if co is None:
        print("Warning: Cohere API key not available. Returning default response.")
        return ["general " + prompt]
    
    try:
        response = co.chat(
            model='command-r-08-2024',
            message=prompt,
            temperature=0.7,
            preamble=preamble
        )

        response_text = response.text
        response_text = response_text.replace("\n", "")
        response_text = response_text.split(",")

        response_text = [i.strip() for i in response_text]

        temp = []

        for task in response_text:
            for func in funcs:
                if task.startswith(func):
                    temp.append(task)
        
        response_text = temp

        if "(query)" in response_text:
            newresponse = FirstLayerDMM(prompt=prompt)
            return newresponse
        else:
            return response_text
    except Exception as e:
        print(f"Error in FirstLayerDMM: {e}")
        return ["general " + prompt]

    
if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>>")))