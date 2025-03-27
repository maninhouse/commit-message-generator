# Commit Message Generator

[English](README.en.md) | [繁體中文](README.md)

A tool that uses Google Gemini API to generate Git commit messages. It provides a REST API interface that receives git diff content and returns appropriate commit message suggestions.

## Features

- Uses Google Gemini API for intelligent analysis
- Provides a REST API interface
- Supports Docker and Docker Compose deployment
- Integrates with Ngrok for temporary public access
- Automatically generates standard-compliant commit messages (currently titles only)

## Installation

### Using Docker Compose (Recommended)

1. Ensure Docker and Docker Compose are installed
2. Copy the environment variables template file:
   ```bash
   cp .env.example .env
   ```
3. Copy the configuration template file:
   ```bash
   cp example-config.json config.json
   ```
4. Edit the `.env` file and set the required environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `NGROK_AUTHTOKEN`: Your Ngrok Authtoken (required for public access)
   - `NGROK_URL`: Your Ngrok domain (optional, for fixed domain)

5. Start the service:
   ```bash
   docker-compose up -d
   ```

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the environment variables template file:
   ```bash
   cp .env.example .env
   ```
3. Copy the configuration template file:
   ```bash
   cp example-config.json config.json
   ```
4. Edit the `.env` file and set the required environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `NGROK_AUTHTOKEN`: Your Ngrok Authtoken (required for public access)
   - `NGROK_URL`: Your Ngrok domain (optional, for fixed domain)
5. Export the environment variables:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   export NGROK_AUTHTOKEN="your-ngrok-authtoken-here"
   export NGROK_URL="your-ngrok-url-here"  # optional
   ```
6. Start the service:
   ```bash
   uvicorn main:app --reload
   ```
   If you encounter an "Address already in use" error, you can use another port:
   ```bash
   uvicorn main:app --reload --port 8080
   ```

## API Usage

### Generate Commit Title

```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"git_diff": "your git diff content"}'
```

### API Documentation

Visit http://localhost:8000/docs to view the complete API documentation.

## Configuration

You can customize by modifying the `config.json` file:

- System instruction (`system_instruction`): Defines the AI model's behavior and prompt content
- Example contents (`example_contents`): Provides examples to help the model understand the task
- Generation parameters (`generate_content_config`): Controls parameters like temperature for AI generation
- Response format (`response_schema`): Defines the structure of the API response

### config.json Parameter Description

```json
{
  "system_instruction": "AI system instruction, defines model behavior",
  "example_contents": [
    {
      "role": "user/model",  // Role: user or model
      "parts": [
        {
          "text": "Q&A template"  // Template for few-shot prompting
        }
      ]
    }
  ],
  "generate_content_config": {
    "temperature": 0.15,  // Controls creativity, lower values are more precise but less diverse
    "response_mime_type": "application/json",  // Response format
    "response_schema": {  // Response structure definition
      "type": "OBJECT",
      "required": ["recommendation"],  // Required fields
      "properties": {
        "options": {  // List of suggestion options
          "type": "ARRAY",
          "items": {
            "type": "STRING"
          }
        },
        "recommendation": {  // Recommended option
          "type": "STRING"
        },
        "explanation": {  // Explanation
          "type": "STRING"
        }
      }
    }
  }
}
```

For first-time use, copy `example-config.json` to `config.json`, then modify as needed.

## Development

Project structure:
```
.
├── main.py
├── core/
│   └── generator.py
├── config.json
├── example-config.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── ngrok.yml
├── README.md
├── restart.sh
└── rebuild.sh
```

## Security Notes

- **NEVER** commit files containing real API keys like `.env` or `config.json` to version control systems
- Set appropriate environment variables before deployment
- Regularly rotate API keys to enhance security

## Additional Notes

- When deployed with Docker Compose, the service automatically restarts (unless manually stopped)
- Ngrok service provides temporary public access, suitable for development and testing
- All sensitive configurations should be set via environment variables or the `.env` file 

## Common Issues

### Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments.

If you encounter this error when using the service, it means the system cannot read the Google Gemini API key. Please check:

1. Confirm that `GEMINI_API_KEY` is correctly set in your `.env` file
2. Verify that the API key format is correct and valid
3. For local installation, make sure you've manually exported the environment variables (see "Local Installation" step 5)
4. Restart the service to ensure environment variables are properly loaded

If you're using the local installation version, you can also try setting the variable directly in your environment:
```bash
export GEMINI_API_KEY="your-api-key-here"
uvicorn main:app --reload
``` 