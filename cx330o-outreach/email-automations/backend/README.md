# cx330o Email Automations — Backend

FastAPI-based service for automated job extraction and cold email generation.

## Features

- Job posting extraction from career websites
- AI-powered cold email generation using CrewAI agents
- Portfolio matching via ChromaDB vector database
- RESTful API with automatic documentation

## Quick Start

```bash
pip install -e .
echo "GROQ_API_KEY=your_key" > .env
python main.py
```

API available at http://localhost:8000

## API Endpoints

- `GET /health` — Health check
- `POST /generate-emails` — Generate personalized cold emails

## Project Structure

```
backend/
├── main.py              # FastAPI entry point
├── src/
│   ├── agents.py        # CrewAI agents
│   ├── portfolio.py     # Portfolio matching
│   └── utils.py         # Utilities
├── resource/            # Portfolio data
└── pyproject.toml       # Dependencies
```

## License

MIT — See LICENSE file.
