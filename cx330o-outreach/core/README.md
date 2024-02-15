# cx330o Outreach — AI Sales Outreach Engine

An AI-powered cold outreach system with research, scoring, and personalized email generation.

## Key Features

- **LangGraph State Machine**: Research → Score → Generate → Send with conditional routing
- **Multi-agent Collaboration**: Researcher + Analyst + Writer working in concert
- **Conversation Tracking**: 8-stage sales conversation model with SPIN questions
- **Multi-CRM Integration**: HubSpot / Airtable / Google Sheets
- **Email Management**: Templates, scheduling, follow-up chains, blacklists
- **Multi-LLM Support**: OpenAI / Groq / any LiteLLM-compatible model

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
python -m outreach_ai --leads leads.csv --mode email
```
