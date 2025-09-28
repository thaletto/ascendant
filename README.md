# Horoscope AI Backend

A prototype backend for AI-powered horoscope predictions and chat functionality built with FastAPI, SQLite, and LangGraph.

## Features

- **User Management**: Store user birth information (name, birth date, time, place)
- **Horoscope Predictions**: Generate daily, weekly, and monthly horoscopes using AI
- **Chat Functionality**: Interactive chat with streaming responses for astrology questions
- **REST API**: Complete REST API with automatic documentation
- **Database**: SQLite database with automatic initialization
- **Agentic AI**: LangGraph-based horoscope generation pipeline

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Copy `env_example.txt` to `.env` and set your OpenAI API key:

```bash
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Application

```bash
python run.py
```

The API will be available at:

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Root & Health

```bash
# Check if API is running
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health
```

### User Management

```bash
# Create a new user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "birth_date": "1990-05-15T00:00:00",
    "birth_time": "14:30",
    "birth_place": "New York, NY"
  }'

# Get user by ID
curl http://localhost:8000/users/1

# List all users
curl http://localhost:8000/users/

# Delete user
curl -X DELETE http://localhost:8000/users/1
```

### Horoscope Predictions

```bash
# Generate daily horoscope
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "prediction_type": "daily"
  }'

# Generate weekly horoscope for specific date
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "prediction_type": "weekly",
    "date": "2024-01-15T00:00:00"
  }'

# Get user's predictions
curl http://localhost:8000/predict/user/1

# Get predictions by type
curl "http://localhost:8000/predict/user/1?prediction_type=daily&limit=5"

# Get specific prediction
curl http://localhost:8000/predict/1

# Delete prediction
curl -X DELETE http://localhost:8000/predict/1
```

### Chat Functionality

```bash
# Stream chat response (using curl with streaming)
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "What does my birth chart say about my career?"
  }' \
  --no-buffer

# Get chat history
curl http://localhost:8000/chat/history/1

# Clear chat history
curl -X DELETE http://localhost:8000/chat/history/1
```

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── db.py                   # Database models and connection
├── models.py               # Pydantic models for API validation
├── horoscope.py            # LangGraph-based horoscope generation
├── routes/                 # API route modules
│   ├── __init__.py
│   ├── users.py           # User management endpoints
│   ├── predictions.py     # Horoscope prediction endpoints
│   └── chat.py            # Chat functionality endpoints
├── requirements.txt        # Python dependencies
├── run.py                 # Simple startup script
├── env_example.txt        # Environment variables template
└── README.md              # This file
```

## Example Usage Flow

1. **Create a user**:

   ```bash
   curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "birth_date": "1995-03-20T00:00:00", "birth_time": "09:15", "birth_place": "Los Angeles, CA"}'
   ```

2. **Generate a horoscope**:

   ```bash
   curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "prediction_type": "daily"}'
   ```

3. **Chat about astrology**:
   ```bash
   curl -X POST "http://localhost:8000/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "message": "Tell me about my sun sign"}' \
     --no-buffer
   ```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for horoscope generation)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `DEBUG`: Enable debug mode (default: false)

### Database

The application uses SQLite by default, which creates a `horoscope_ai.db` file in the project directory. The database is automatically initialized when the application starts.

## Development

### Running in Development Mode

```bash
python run.py
```

This will start the server with auto-reload enabled.

### Running with Uvicorn Directly

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Notes

- The horoscope generation uses OpenAI's GPT-3.5-turbo model
- All horoscope predictions are stored in the database
- Chat responses are streamed in real-time
- The application is designed to be easily extensible for more complex astrological calculations
- All endpoints are fully documented and validated using Pydantic models

## Troubleshooting

1. **OpenAI API Key Error**: Make sure you've set the `OPENAI_API_KEY` environment variable
2. **Database Errors**: Ensure the application has write permissions in the project directory
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
