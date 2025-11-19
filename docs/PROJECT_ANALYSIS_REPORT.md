# Jasmine AI Assistant - Project Analysis Report

## Overview

Jasmine AI is an advanced personal assistant application with voice interaction capabilities, powered by artificial intelligence. The system is designed to understand natural language queries, perform tasks, provide information, and engage in conversations with users through both text and speech interfaces.

## Architecture

The project follows a modular architecture with clearly separated components:

### 1. Core Structure
```
Jasmine_ai-main/
├── Backend/              # AI and automation modules
├── Frontend/             # Graphical user interface
├── Data/                 # Persistent data storage
├── .env                  # Configuration file
├── Main.py               # Primary entry point
├── Requirements.txt      # Dependencies
└── Documentation files   # Setup and usage guides
```

### 2. Backend Components

#### Decision Making Model (Model.py)
- Uses Cohere API for natural language understanding
- Classifies user queries into categories:
  - General queries (conversational)
  - Real-time queries (requiring current information)
  - Task automation (opening apps, playing media)
  - Mathematical operations
  - Content generation
  - System commands
  - Exit commands

#### Chatbot (Chatbot.py)
- Primary conversational interface
- Integrates with Google Gemini API for intelligent responses
- Maintains conversation history in ChatLog.json
- Handles emotional intelligence and appropriate responses

#### Real-time Search Engine (RealtimeSearchEngine.py)
- Performs web searches using Google Search
- Processes search results with Gemini API for coherent answers
- Includes specialized weather information handling via Open-Meteo API

#### Speech Processing
- SpeechToText.py: Converts voice to text using browser-based recognition
- TextToSpeech.py: Converts text to speech using Murf API or Edge TTS

#### Specialized Modules
- Mathematics.py: Handles mathematical operations using SymPy
- Automation.py: System automation tasks (opening/closing apps, system commands)
- ImageGeneration.py: Generates images using Hugging Face Stable Diffusion
- GeminiAPI.py: Central interface to Google's Gemini AI model

### 3. Frontend Component

#### GUI (GUI.py)
- PyQt-based graphical interface
- Displays conversation history
- Provides microphone control
- Shows assistant status

### 4. Data Management

#### Persistent Storage
- ChatLog.json: Conversation history
- Mic.data: Microphone status
- Status.data: Assistant status
- Responses.data: Current assistant responses

## Workflow

### 1. Initialization
1. Load environment variables from .env file
2. Initialize all backend modules
3. Set up data directories and files
4. Launch GUI interface

### 2. Main Execution Loop
1. Monitor microphone status
2. When active, capture voice input through SpeechToText
3. Process query through Decision Making Model
4. Route query to appropriate handler:
   - General queries → Chatbot
   - Real-time queries → Search Engine
   - Math queries → Mathematics module
   - Automation tasks → Automation module
5. Generate response through TextToSpeech
6. Update conversation history

### 3. Query Processing Flow
1. User speaks query or types text
2. SpeechToText converts audio to text
3. Model.py classifies query type
4. Appropriate backend module processes query
5. Response generated and formatted
6. TextToSpeech converts response to audio
7. Response displayed in GUI and spoken aloud

## Key Features

### AI Capabilities
- Natural language understanding and generation
- Context-aware conversations with history tracking
- Mathematical problem solving
- Code explanation and debugging
- Image generation capabilities
- Real-time information retrieval

### Voice Interaction
- Speech-to-text conversion
- Text-to-speech synthesis
- Microphone control
- Multi-language support

### Automation
- Application opening/closing
- Media playback
- System commands (volume control)
- Content generation (letters, documents)

### Specialized Functions
- Weather information retrieval
- Mathematical calculations
- Image generation
- Code assistance

## Technology Stack

### Core Technologies
- Python 3.x
- Google Gemini API
- Cohere API
- PyQt for GUI
- Selenium for web automation

### Key Libraries
- google-generativeai: Gemini API integration
- cohere: Decision making model
- pygame: Audio playback
- edge-tts: Text-to-speech
- sympy: Mathematical operations
- requests: HTTP requests
- dotenv: Environment management

### Platform Support
- Cross-platform design (Windows, macOS, Linux)
- Platform-specific optimizations where needed

## API Integrations

### Google Gemini
- Primary AI model for conversations
- Mathematical problem solving
- Code assistance
- Image analysis capabilities

### Cohere
- Decision making and query classification

### Murf/Edge TTS
- Text-to-speech synthesis

### Open-Meteo
- Weather information

### Hugging Face
- Image generation

## Configuration

### Environment Variables (.env)
- API keys for services (Gemini, Cohere, Groq, Murf)
- User preferences (name, voice settings)
- Language settings

### Customization
- User and assistant names
- Voice preferences
- Language settings
- API key configuration

## Data Flow

1. **Input**: Voice or text query from user
2. **Processing**: 
   - Speech recognition (if voice input)
   - Query classification (Model.py)
   - Specialized processing (appropriate module)
3. **Response Generation**: 
   - AI-powered response (Gemini API)
   - Response formatting
4. **Output**: 
   - Text display in GUI
   - Speech synthesis
   - Conversation logging

## Error Handling

- Graceful degradation when APIs are unavailable
- Fallback mechanisms for critical functions
- Detailed error logging
- User-friendly error messages

## Security

- API keys stored in .env file (not committed to version control)
- Secure handling of user data
- No transmission of sensitive information

## Performance Considerations

- Caching mechanisms for frequently requested information
- Efficient conversation history management
- Optimized API usage to minimize latency
- Asynchronous processing where appropriate

## Extensibility

- Modular design allows for easy addition of new features
- Clear separation of concerns
- Well-defined interfaces between components
- Plugin architecture for additional functionality

## Limitations

- Platform-specific features (some automation only works on Windows)
- Dependency on external API services
- Requires proper API key configuration
- Internet connectivity required for most features

## Setup Requirements

1. Python 3.7+
2. Required packages from Requirements.txt
3. API keys for Gemini, Cohere, and other services
4. Proper audio device configuration
5. Chrome browser for speech recognition

## Usage

1. Configure .env with API keys
2. Install dependencies: `pip install -r Requirements.txt`
3. Run: `python Main.py`
4. Activate microphone: `python toggle_microphone.py true`
5. Speak or type queries to interact

This comprehensive analysis shows that Jasmine AI is a sophisticated personal assistant with robust AI capabilities, voice interaction, and automation features, designed for cross-platform compatibility with a modular, extensible architecture.