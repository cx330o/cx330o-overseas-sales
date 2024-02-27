# cx330o Email Automations

Multi-agent cold email generation system for the cx330o Sales Platform.

## Features

- Web scraping of job postings from career websites
- AI-powered job requirement analysis
- Multi-agent system (Job Analyst, Portfolio Analyst, Email Writer, Coordinator)
- Portfolio matching via vector database (ChromaDB)
- Personalized cold email generation
- React frontend with real-time progress
- History tracking for generated emails

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > .env
python main.py

# Frontend
cd frontend
npm install
npm start
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Tech Stack

- Backend: FastAPI, CrewAI, LangChain, ChromaDB, Groq
- Frontend: React 18, Tailwind CSS, Axios

## License

MIT — See root LICENSE file.
