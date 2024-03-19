# cx330o Email Generator

Fast LLM-powered cold email generator for the cx330o Sales Platform.

## Features

- URL-based job listing extraction from career pages
- Personalized cold email generation using LLM
- Portfolio link matching from vector database
- Streamlit web interface

## Quick Start

```bash
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > app/.env
streamlit run app/main.py
```

## Tech Stack

- Groq for fast LLM inference
- LangChain for orchestration
- ChromaDB for vector storage
- Streamlit for web UI

## License

MIT — See root LICENSE file.
