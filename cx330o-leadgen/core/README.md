# cx330o LeadGen — Unified Lead Generation Engine

A powerful multi-source lead scraping toolkit with AI enrichment capabilities.

## Key Features

- **Async Plugin Architecture**: Each data source is a pluggable Engine with async fetching
- **Multi-source Aggregation**: Google Maps + Yelp + OSINT (emails/domains/subdomains)
- **Deep Parsing**: Review/rating/multi-language parsing with pagination support
- **AI Enrichment**: LLM-powered data enrichment pipeline
- **Unified Output**: CSV / JSON / Google Sheets / Database with consistent data models
- **Anti-scraping**: Rate limiting, proxy rotation, User-Agent randomization
- **Data Quality**: Deduplication, validation, cleaning

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env  # Fill in API keys
python -m lead_gen_pro --source google_maps --query "restaurants" --location "New York"
```

## Supported Engines

| Engine | Data Type | Description |
|--------|-----------|-------------|
| GoogleMapsEngine | Business info + reviews | Playwright-based async scraping |
| YelpEngine | Business info | Search result extraction |
| OSINTEngine | Emails/domains/subdomains | Multi-source intelligence gathering |
| AIEnricher | AI enrichment | LLM-powered analysis and personalization |
