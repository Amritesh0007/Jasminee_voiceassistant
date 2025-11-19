import platform
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import asyncio
import os
import subprocess
import requests
from dotenv import dotenv_values

# Load environment variables with absolute path
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)

Assistantname = env_vars.get("Assistantname")

# Platform detection
CURRENT_PLATFORM = platform.system().lower()

# Try to import optional modules
APPOPENER_AVAILABLE = False
PYWHATKIT_AVAILABLE = False
KEYBOARD_AVAILABLE = False

try:
    if CURRENT_PLATFORM == "windows":
        from AppOpener import close, open as appopen
        APPOPENER_AVAILABLE = True
except ImportError:
    pass

# Handle pywhatkit import error gracefully
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("Warning: pywhatkit not available. Some features may be limited.")
except Exception as e:
    PYWHATKIT_AVAILABLE = False
    print(f"Warning: pywhatkit import failed with error: {e}")

# Import pyautogui only if pywhatkit is available
if PYWHATKIT_AVAILABLE:
    try:
        import pyautogui
    except ImportError:
        print("Warning: pyautogui not available. Some pywhatkit features may be limited.")
    except Exception as e:
        print(f"Warning: pyautogui import failed with error: {e}")

# Only import keyboard on Windows to avoid issues on macOS
if CURRENT_PLATFORM == "windows":
    try:
        import keyboard
        KEYBOARD_AVAILABLE = True
    except ImportError:
        pass

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Clean up the API key if it exists
if GroqAPIKey:
    GroqAPIKey = GroqAPIKey.strip().strip('"').strip("'")

classes = ["zCubwf", "hgKELc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", 
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client only if API key exists
client = None
if GroqAPIKey:
    client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username', 'User')}, a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."}]


def GoogleSearch(topic):
    # Always use web browser for search
    url = f"https://www.google.com/search?q={topic}"
    webbrowser.open(url)
    return True


def Content(topic):
    def OpenNotepad(file):
        try:
            if CURRENT_PLATFORM == "windows":
                default_text_editor = 'notepad.exe'
                subprocess.Popen([default_text_editor, file])
            elif CURRENT_PLATFORM == "darwin":  # macOS
                subprocess.Popen(['open', '-a', 'TextEdit', file])
            else:  # Linux and others
                # Try common text editors
                editors = ['gedit', 'nano', 'vim', 'emacs']
                for editor in editors:
                    try:
                        subprocess.Popen([editor, file])
                        break
                    except FileNotFoundError:
                        continue
        except Exception as e:
            print(f"Error opening text editor: {e}")

    def ContentWriterAI(prompt):
        if not client:
            print("Error: Groq API key not found. Please check your .env file.")
            return "Error: Unable to generate content - API key missing."
        
        try:
            user_message = {"role": "user", "content": prompt}
            messages.append(user_message)

            # Create properly formatted messages for Groq API
            formatted_messages = []
            for msg in SystemChatBot:
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})
            
            for msg in messages:
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=formatted_messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=False
            )

            answer = completion.choices[0].message.content or ""
            answer = answer.replace("</s>", "")
            assistant_message = {"role": "assistant", "content": answer}
            messages.append(assistant_message)
            return answer
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error: Unable to generate content - {str(e)}"

    topic = topic.replace("content", "").strip()
    content_by_ai = ContentWriterAI(topic)

    # Create Data directory if it doesn't exist
    data_dir = "Data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, f"{topic.lower().replace(' ', '_')}.txt")
    
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content_by_ai)
        
        OpenNotepad(filepath)
        return True
    except Exception as e:
        print(f"Error writing content to file: {e}")
        return False

def YouTubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True


def PlayYoutube(query):
    # Always use web browser for YouTube
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return True


def PlaySongInApp(song_name, app_name):
    """Play a song in a specific application"""
    # For now, we'll default to YouTube search for any song
    # In a more advanced implementation, we could integrate with specific music services
    search_query = f"{song_name} {app_name}"
    return PlayYoutube(search_query)


def OpenApp(app, sess=requests.session()):
    # Platform-specific app opening
    if CURRENT_PLATFORM == "windows" and APPOPENER_AVAILABLE:
        try:
            # Try to open the app using AppOpener
            globals()['appopen'](app, match_closest=True, output=True)
            return True
        except Exception as e:
            print(f"AppOpener failed: {e}")
    elif CURRENT_PLATFORM == "darwin":  # macOS
        try:
            # Common app name mappings for macOS
            app_mappings = {
                "notepad": "TextEdit",
                "text editor": "TextEdit",
                "calculator": "Calculator",
                "calendar": "Calendar",
                "contacts": "Contacts",
                "mail": "Mail",
                "safari": "Safari",
                "chrome": "Google Chrome",
                "firefox": "Firefox",
                "spotify": "Spotify",
                "vlc": "VLC",
                "photos": "Photos",
                "messages": "Messages",
                "facetime": "FaceTime",
                "maps": "Maps",
                "weather": "Weather",
                "notes": "Notes",
                "reminders": "Reminders",
                "terminal": "Terminal",
                "activity monitor": "Activity Monitor",
                "system preferences": "System Preferences",
                "app store": "App Store"
            }
            
            # Check if we have a mapping for this app
            mapped_app = app_mappings.get(app.lower(), app)
            mac_app_name = mapped_app if mapped_app is not None else app
            
            # Try to open the app
            if mac_app_name:
                result = subprocess.run(["open", "-a", str(mac_app_name)], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Opened {mac_app_name} successfully")
                    return True
                else:
                    print(f"Failed to open {mac_app_name}: {result.stderr}")
                    # Try with title case
                    mac_app_name_title = str(mac_app_name).title() if mac_app_name else ""
                    if mac_app_name_title:
                        result = subprocess.run(["open", "-a", str(mac_app_name_title)], capture_output=True, text=True)
                        if result.returncode == 0:
                            print(f"Opened {mac_app_name_title} successfully")
                            return True
                        else:
                            print(f"Failed to open {mac_app_name_title}: {result.stderr}")
        except Exception as e:
            print(f"Error opening app {app}: {e}")
    elif CURRENT_PLATFORM == "linux":
        try:
            # Try common Linux methods
            subprocess.run(["xdg-open", app], check=True)
            return True
        except subprocess.CalledProcessError:
            pass
    
    # Fallback: search for the app online
    def extract_links(html):
        if html is None:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        # Find all anchors with valid href attributes
        links = soup.find_all('a', href=True)
        return [link.get('href') for link in links]
        
    def search_google(query):
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = sess.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to retrieve search results.")
            return None

    def open_in_browser(url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening browser: {e}")
            return False

    # Attempt a search for the app
    html = search_google(app)
    if html:
        links = extract_links(html)
        if links:
            link = links[0]
            open_in_browser(link)
    return True

def CloseApp(app):
    # Platform-specific app closing
    if CURRENT_PLATFORM == "windows" and APPOPENER_AVAILABLE:
        if "chrome" in app.lower():
            try:
                subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], check=True)
                print(f"Closed Chrome using taskkill")
                return True
            except:
                pass
        
        try:
            globals()['close'](app, match_closest=True, output=True)
            print(f"Closed {app} using AppOpener")
            return True
        except Exception as e:
            print(f"Error closing {app}: {e}")
            return False
    elif CURRENT_PLATFORM == "darwin":  # macOS
        try:
            # Common app name mappings for macOS
            app_mappings = {
                "notepad": "TextEdit",
                "text editor": "TextEdit",
                "calculator": "Calculator",
                "calendar": "Calendar",
                "contacts": "Contacts",
                "mail": "Mail",
                "safari": "Safari",
                "chrome": "Google Chrome",
                "firefox": "Firefox",
                "spotify": "Spotify",
                "vlc": "VLC",
                "photos": "Photos",
                "messages": "Messages",
                "facetime": "FaceTime",
                "maps": "Maps",
                "weather": "Weather",
                "notes": "Notes",
                "reminders": "Reminders",
                "terminal": "Terminal",
                "activity monitor": "Activity Monitor",
                "system preferences": "System Preferences",
                "app store": "App Store"
            }
            
            # Check if we have a mapping for this app
            mapped_app = app_mappings.get(app.lower(), app)
            mac_app_name = mapped_app if mapped_app is not None else app
            
            # Use macOS 'osascript' to quit app
            if mac_app_name:
                subprocess.run(["osascript", "-e", f'quit app "{str(mac_app_name)}"'], check=True)
                print(f"Closed {mac_app_name} using osascript")
                return True
            else:
                print(f"Could not determine app name for {app}")
                return False
        except subprocess.CalledProcessError as e:
            # Special handling for Chrome
            if "chrome" in app.lower():
                try:
                    # Try alternative method to close Chrome
                    subprocess.run(["pkill", "Google Chrome"], check=True)
                    print(f"Closed Chrome using pkill")
                    return True
                except subprocess.CalledProcessError:
                    print(f"Error closing {app} on macOS: {e}")
                    return False
            else:
                print(f"Error closing {app} on macOS: {e}")
                return False
        except Exception as e:
            print(f"Unexpected error closing {app} on macOS: {e}")
            return False
    elif CURRENT_PLATFORM == "linux":
        try:
            # Try to kill process by name
            subprocess.run(["pkill", "-f", app], check=True)
            print(f"Closed {app} using pkill")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error closing {app} on Linux: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error closing {app} on Linux: {e}")
            return False
    else:
        print(f"App closing not supported on {CURRENT_PLATFORM}")
        return False


def System(command):
    # Only support system commands on Windows for now
    if CURRENT_PLATFORM != "windows" or not KEYBOARD_AVAILABLE:
        print(f"System commands not supported on {CURRENT_PLATFORM}")
        return False
    
    # Use conditional access to keyboard module
    if 'keyboard' in globals():
        try:
            if command == "mute":
                globals()['keyboard'].press_and_release("volume mute")
            elif command == "unmute":
                globals()['keyboard'].press_and_release("volume mute")
            elif command == "volume up":
                globals()['keyboard'].press_and_release("volume up")
            elif command == "volume down":
                globals()['keyboard'].press_and_release("volume down")
            else:
                print(f"Unknown system command: {command}")
                return False
            
            print(f"Executed system command: {command}")
            return True
        except Exception as e:
            print(f"Error executing system command {command}: {e}")
            return False
    else:
        print("Keyboard module not available")
        return False


async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open and search "):
            # Handle "open and search chrome" - we need to extract the search query from context
            # For now, we'll just open the app and do a generic search
            app_name = command.removeprefix("open and search ").strip()
            # For commands like "search python on chrome", we should have detected "google search python" instead
            # But since we're getting this format, let's just open the app
            fun = asyncio.to_thread(OpenApp, app_name)
            funcs.append(fun)
        elif command.startswith("open and play "):
            # Handle "open and play spotify" - we need to extract the song name from context
            # For now, we'll just open the app
            app_name = command.removeprefix("open and play ").strip()
            # For commands like "play humnava music on spotify", we should have detected "play humnava music" instead
            # But since we're getting this format, let's just open the app
            fun = asyncio.to_thread(OpenApp, app_name)
            funcs.append(fun)
        elif command.startswith("open "):
            app_name = command.removeprefix("open ").strip()
            # Special handling for web services - open in browser
            if app_name.lower() in ["youtube", "youtube music"]:
                fun = asyncio.to_thread(PlayYoutube, "")
            elif app_name.lower() in ["gmail", "google mail"]:
                fun = asyncio.to_thread(webbrowser.open, "https://mail.google.com")
            elif app_name.lower() in ["google drive", "drive"]:
                fun = asyncio.to_thread(webbrowser.open, "https://drive.google.com")
            elif app_name.lower() in ["google docs", "docs"]:
                fun = asyncio.to_thread(webbrowser.open, "https://docs.google.com")
            elif app_name.lower() in ["google sheets", "sheets"]:
                fun = asyncio.to_thread(webbrowser.open, "https://sheets.google.com")
            elif app_name.lower() in ["google slides", "slides"]:
                fun = asyncio.to_thread(webbrowser.open, "https://slides.google.com")
            elif app_name.lower() in ["google photos", "photos"]:
                fun = asyncio.to_thread(webbrowser.open, "https://photos.google.com")
            elif app_name.lower() in ["google maps", "maps"]:
                fun = asyncio.to_thread(webbrowser.open, "https://maps.google.com")
            else:
                fun = asyncio.to_thread(OpenApp, app_name)
            funcs.append(fun)
        elif command.startswith("close "):
            app_name = command.removeprefix("close ").strip()
            fun = asyncio.to_thread(CloseApp, app_name)
            funcs.append(fun)
        elif command.startswith("play "):
            query = command.removeprefix("play ").strip()
            fun = asyncio.to_thread(PlayYoutube, query)
            funcs.append(fun)
        elif command.startswith("content "):
            topic = command.removeprefix("content ").strip()
            fun = asyncio.to_thread(Content, topic)
            funcs.append(fun)
        elif command.startswith("google search "):
            query = command.removeprefix("google search ").strip()
            fun = asyncio.to_thread(GoogleSearch, query)
            funcs.append(fun)
        elif command.startswith("youtube search "):
            query = command.removeprefix("youtube search ").strip()
            fun = asyncio.to_thread(YouTubeSearch, query)
            funcs.append(fun)
        elif command.startswith("system "):
            sys_command = command.removeprefix("system ").strip()
            # Only execute system commands on Windows
            if CURRENT_PLATFORM == "windows":
                fun = asyncio.to_thread(System, sys_command)
                funcs.append(fun)

    if funcs:
        results = await asyncio.gather(*funcs, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"Command failed with exception: {result}")
            else:
                print(f"Command result: {result}")
        return results
    else:
        print("No valid commands to execute")
        return []


async def Automation(commands: list[str]):
    results = await TranslateAndExecute(commands)
    return True


# if __name__ == "__main__":
#     # Test with some commands
#     test_commands = [
#         "open notepad", 
#         " content application for sick leave"
#     ]
    
#     print("Testing automation...")
#     asyncio.run(Automation(test_commands))