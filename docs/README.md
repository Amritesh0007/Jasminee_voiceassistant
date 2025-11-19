# Jasmine AI - Enhanced with Google Gemini API

An advanced AI assistant with integrated Google Gemini API capabilities.

## Key Features Implemented

### 🚀 Google Gemini API Integration
- **Text Generation**: Advanced content creation and summarization
- **Chat Completions**: Context-aware conversational AI
- **Mathematical Problem Solving**: Complex calculations and explanations
- **Code Assistance**: Code explanation, debugging, and review
- **Multimodal Capabilities**: Ready for image analysis (vision AI)
- **Optimized Performance**: Faster response times with caching and efficient processing
- **Direct Weather Information**: Accurate temperature and forecast data using Open-Meteo API

### 💝 Enhanced Emotional Intelligence
- Improved handling of emotional expressions with appropriate empathy
- Better distinction between translation requests and emotional expressions
- Context-aware responses that maintain appropriate boundaries

### 🗣️ Improved Text-to-Speech
- Slower speech rate for better comprehension (20% slower)
- Enhanced pause management for natural speech flow
- Better handling of emotional responses without breaking gaps
- Retry logic for more reliable audio generation

### 🔍 Advanced Search Capabilities
- Real-time information retrieval with Gemini-powered processing
- Fallback mechanisms for search service reliability

## Setup Instructions

1. **Add your API Keys** to `.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r Requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python Main.py
   ```

## Documentation
- [GEMINI_INTEGRATION.md](GEMINI_INTEGRATION.md) - Detailed Gemini API integration guide
- [USAGE_INSTRUCTIONS.md](USAGE_INSTRUCTIONS.md) - General usage instructions

## Recent Improvements
- Fixed translation request handling (no longer confused with emotional expressions)
- Enhanced TTS with better pause management and slower speech rate
- Improved reliability with retry logic for audio services
- Better context awareness in conversations
- **Performance Optimizations**: Faster response times with caching, reduced conversation history, and optimized model selection
- **Direct Weather Information**: Accurate temperature and forecast data without relying on search results

## API Functions Available
- `generate_text(prompt, temperature)` - Generate text from a prompt
- `chat_completion(messages, temperature)` - Multi-turn chat completion
- `solve_math_problem(problem)` - Solve mathematical problems
- `explain_code(code, language)` - Explain code functionality
- `debug_code(code, error, language)` - Help debug code issues

For more details, see [GEMINI_INTEGRATION.md](GEMINI_INTEGRATION.md).