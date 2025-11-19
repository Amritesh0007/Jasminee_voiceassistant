# Gemini API Integration for Jasmine AI

This document explains how to use the Gemini API integration in the Jasmine AI assistant.

## Setup Instructions

1. **Add your API Key**: 
   - Copy the `.env.template` file to `.env` in the project root
   - Replace `your_gemini_api_key_here` with your actual Gemini API key:
     ```
     GEMINI_API_KEY = "AIzaSyCA69QvhM8OkY2ttVMcGXmyhmgHQI4ghSM"
     ```

2. **Install Dependencies**:
   Run the following command to install the required dependencies:
   ```bash
   pip install -r Requirements.txt
   ```

## Features Implemented

### 1. Text Generation
Generate essays, articles, summaries, and creative content.

### 2. Enhanced Chat Responses
The assistant now uses Gemini for more natural and contextual conversations.

### 3. Advanced Mathematical Problem Solving
Gemini handles complex mathematical computations and explanations.

### 4. Code Assistance
- Code explanation
- Debugging assistance
- Code review

### 5. Multimodal Capabilities
- Image analysis (vision capabilities)
- Combined text and image processing

## Usage Examples

### Direct API Usage
```python
from Backend.GeminiAPI import generate_text, solve_math_problem

# Generate text
response = generate_text("Explain quantum computing in simple terms")
print(response)

# Solve math problems
solution = solve_math_problem("Integrate x^2 from 0 to 5")
print(solution)
```

### Running Demos
```bash
python gemini_demo.py
```

## Integration Details

The Gemini API is integrated into the main assistant flow:

1. **Enhanced Conversations**: All general queries are now processed through Gemini for more natural responses
2. **Mathematical Processing**: Complex math queries are handled by Gemini with fallback to the existing system
3. **Context Awareness**: The assistant maintains conversation history for contextual responses

## API Functions Available

- `generate_text(prompt, temperature)`: Generate text from a prompt
- `chat_completion(messages, temperature)`: Multi-turn chat completion
- `analyze_image(image_path, prompt)`: Analyze images using Gemini Vision
- `solve_math_problem(problem)`: Solve mathematical problems
- `explain_code(code, language)`: Explain code functionality
- `debug_code(code, error, language)`: Help debug code issues

## Troubleshooting

1. **API Key Issues**:
   - Ensure your API key is correctly placed in the `.env` file
   - Verify the key has the necessary permissions

2. **Dependency Issues**:
   - Run `pip install google-generativeai` if you encounter import errors

3. **Rate Limiting**:
   - Gemini APIs have rate limits; implement appropriate delays if making many requests

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- The `.env.template` file is safe to commit as it doesn't contain real keys