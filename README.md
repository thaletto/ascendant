# Ascendant - AI Astrology Intelligence System

A modular, multi-astrology intelligence system designed to perform advanced astrological analysis, chart synthesis, and contextual reasoning. Built with FastAPI, SQLite, and Google ADK.

## Features

- **Modular Agent Architecture**: Specialized agents for different astrology domains
- **Comprehensive Chart Analysis**: Rasi, Saptamsha, Navamsha, Dasamsha, and custom divisional charts
- **Vimshottari Dasha Analysis**: Complete planetary period calculations and predictions
- **Planetary Analysis**: Positions, aspects, relationships, and strength analysis
- **Specialized Predictions**: Health, career, wealth, marriage, family, emotion, love, and children
- **User Management**: Store user birth information with session tracking
- **REST API**: Complete REST API with automatic documentation
- **Database**: SQLite database with automatic initialization
- **Memory Efficient**: On-demand object reconstruction with proper cleanup

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

## Agent Architecture

**Root Agent** (General Reasoning & Context Manager)

- ChartAgent (Rasi Chart, Saptamsa, Navamsha, etc...)
- DashaAgent (Vimshottari Dasha Analysis)
- YogaAgent (Yogam Analysis)
- PlanetAgent (Positions & Relationships)
- TransitAgent (Current Influence)
- RemedyAgent (Remedial Insights)

## Project Structure

```
Ascendant/
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
│   ├── agent.py                    # Root agent (coordinates all specialists)
│   ├── agents/
│   │   ├── chart_agent.py          # ChartAgent - divisional charts
│   │   ├── dasha_agent.py          # DashaAgent - planetary periods
│   │   ├── planet_agent.py         # PlanetAgent - positions & aspects
│   │   └── __init__.py
│   ├── config/
│   │   └── models.py
│   └── tools/
│       └── horoscope.py            # Centralized astrology tools
├── README.md
├── AGENT.md                        # Architecture documentation
├── requirements.txt
└── run.py
```

## API Endpoints

### Prediction

- `/predict` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (user's astrology question/request)

- `/predict/health` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (health-related astrology question/request)

- `/predict/career` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (career-related astrology question/request)

- `/predict/wealth` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (wealth-related astrology question/request)

- `/predict/marriage` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (marriage-related astrology question/request)

- `/predict/family` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (family-related astrology question/request)

- `/predict/emotion` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (emotion-related astrology question/request)

- `/predict/love` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (love-related astrology question/request)

- `/predict/children` [POST]
  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (children-related astrology question/request)

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

## Key Features

### Modular Agent Architecture
- **Root Agent**: Coordinates all specialized agents for comprehensive analysis
- **ChartAgent**: Handles divisional charts (D1, D7, D9, D10, custom divisions)
- **DashaAgent**: Manages Vimshottari Dasha analysis and planetary periods
- **PlanetAgent**: Analyzes planetary positions, aspects, and relationships

### Memory Efficiency
- On-demand object reconstruction from serialized birth data
- Automatic cleanup to prevent memory leaks
- Efficient resource management across all agents

### Specialized Predictions
- Health, Career, Wealth, Marriage, Family, Emotion, Love, Children
- Domain-specific endpoints for targeted astrological insights
- Session-based context management

## Notes

- OpenRouter acts as the model provider
- All horoscope predictions are stored in the database
- Chat responses are streamed in real-time
- The application uses a modular architecture for easy extensibility
- All endpoints are fully documented and validated using Pydantic models
- Centralized tools prevent code duplication and ensure consistency

## Troubleshooting

1. **OpenRouter API Key Error**: Make sure you've set the `OPENROUTER_API_KEY` environment variable
2. **Database Errors**: Ensure the application has write permissions in the project directory
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
4. **Agent Import Errors**: Verify that all agent modules are properly configured in the horoscope_agent package
