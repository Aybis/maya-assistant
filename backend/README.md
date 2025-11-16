# Maya Assistant Backend

FastAPI backend for the Maya Assistant multi-AI chat application.

## Features

- **RESTful API**: Clean and well-documented API endpoints
- **Streaming Responses**: Server-Sent Events for real-time AI streaming
- **Multi-AI Support**: Integrated with OpenAI, Anthropic, and Google AI
- **Authentication**: JWT-based auth via Supabase
- **Database**: PostgreSQL via Supabase with Row Level Security
- **Type Safety**: Pydantic models for validation

## Installation

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Running

Development mode with auto-reload:
```bash
uvicorn app.main:app --reload
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/              # API route handlers
├── models/           # Pydantic models
├── services/         # Business logic
├── utils/            # Utilities
├── config.py         # Settings
├── dependencies.py   # FastAPI dependencies
└── main.py          # Application entry point
```

## Testing

```bash
pytest
```

## Environment Variables

See `.env.example` for required variables.
