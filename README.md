# Horoscope AI Backend

A prototype backend for AI-powered horoscope predictions and chat functionality built with FastAPI, SQLite, and Google ADK.

## Features

- **User Management**: Store user birth information (name, birth date, time, place)
- **Horoscope Predictions**: Generate daily, weekly, and monthly horoscopes using AI
- **Chat Functionality**: Interactive chat with streaming responses for astrology questions
- **REST API**: Complete REST API with automatic documentation
- **Database**: SQLite database with automatic initialization
- **Agentic AI**: Google ADK-based horoscope generation pipeline

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

## Project Structure

```
Ascendant-AI/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── prediction.py
│   │       └── users.py
│   ├── db/
│   │   ├── client.py
│   │   └── schema.py
│   ├── main.py
│   ├── models/
│   │   └── users.py
│   └── utils/
│       ├── chart.py
│       ├── dasha.py
│       ├── planets.py
│       └── yoga.py
├── config.py
├── horoscope_agent/
│   ├── agent.py
│   ├── config/
│   │   └── models.py
│   └── tools/
│       └── horoscope.py
├── README.md
├── requirements.txt
└── run.py
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

- OpenRouter acts as the model provider
- All horoscope predictions are stored in the database
- Chat responses are streamed in real-time
- The application is designed to be easily extensible for more complex astrological calculations
- All endpoints are fully documented and validated using Pydantic models

## Troubleshooting

1. **OpenRouter API Key Error**: Make sure you've set the `OPENROUTER_API_KEY` environment variable
2. **Database Errors**: Ensure the application has write permissions in the project directory
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
