# cx330o LiveChat

Omnichannel customer support and live chat module for the cx330o Sales Platform.

## Features

- Live chat widget for websites
- Omnichannel inbox (email, Facebook, Instagram, Twitter, WhatsApp, Telegram, LINE, SMS)
- AI-powered auto-responses
- Canned responses and macros
- Team collaboration and assignment rules
- Help center / knowledge base portal
- Customer satisfaction surveys
- Reporting and analytics

## Usage

```bash
# Part of the full platform
docker compose up -d
# Access at http://localhost:3011 (standalone) or via Marketing Gateway
```

## Architecture

Ruby on Rails application with React frontend. Uses PostgreSQL and Redis.
Integrates with the cx330o Marketing Gateway for unified API access.

## License

See root LICENSE file.
