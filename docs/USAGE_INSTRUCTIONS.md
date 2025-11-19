# Jarvis AI Assistant - Usage Instructions

## Getting Started

1. **Run the Application**:
   ```bash
   cd /Users/amriteshkumar/Jarvis/jarvis-ai-assistant
   python3 Main.py
   ```

2. **Activate Voice Recognition**:
   ```bash
   python3 toggle_microphone.py true
   ```

3. **Speak to the Assistant**:
   - The application will open a Chrome browser window for speech recognition
   - Speak clearly into your microphone
   - The assistant will respond both in text and speech

## Voice Commands

The assistant can handle various types of queries:

### General Conversations
- "Hello, how are you?"
- "What's the weather like today?"
- "Tell me a joke"

### Real-time Information
- "Who is the current president?"
- "What's the latest news?"
- "What time is it in London?"

### Task Automation
- "Open notepad" (Opens TextEdit on macOS)
- "Open chrome" (Opens Google Chrome)
- "Play some music" (Opens YouTube search)
- "Close Chrome"
- "Search for Python tutorials on YouTube"
- "Google search artificial intelligence"

### Content Generation
- "Write an application for sick leave"
- "Generate a poem about nature"
- "Create a shopping list"

## Troubleshooting

### Microphone Not Working
1. Check microphone status:
   ```bash
   cat Frontend/Files/Mic.data
   ```
2. Activate microphone if needed:
   ```bash
   python3 toggle_microphone.py true
   ```

### Chrome Browser Issues
1. Make sure Chrome is installed
2. Allow microphone permissions when prompted
3. Check that Chrome can access your microphone in system preferences

### No Response from Assistant
1. Check that the microphone is activated ("True" in Mic.data)
2. Speak clearly and at a moderate pace
3. Check the terminal for status updates
4. Ensure all required packages are installed:
   ```bash
   pip3 install -r requirements.txt
   ```

### Application Opening Issues
The assistant now supports opening applications on macOS with these mappings:
- "notepad" → TextEdit
- "chrome" → Google Chrome
- "calculator" → Calculator
- "calendar" → Calendar
- "mail" → Mail
- "safari" → Safari
- "spotify" → Spotify
- "terminal" → Terminal

## File Structure

- `.env` - Configuration file with API keys and settings
- `Data/` - Directory for chat logs and temporary files
- `Frontend/Files/` - GUI status and communication files
- `Backend/` - AI and automation modules

## Status Files

- `Frontend/Files/Mic.data` - Microphone status ("True"/"False")
- `Frontend/Files/Status.data` - Assistant status
- `Frontend/Files/Responses.data` - Assistant responses
- `Data/ChatLog.json` - Conversation history

## Exiting the Application

1. Close the GUI window
2. Or press Ctrl+C in the terminal

## Tips for Best Experience

1. Speak clearly and at a moderate pace
2. Use specific queries for better results
3. Allow microphone access when prompted by Chrome
4. Check the terminal for status updates
5. Responses will appear in both the GUI and will be spoken aloud
6. For application opening, use simple names like "notepad", "chrome", etc.