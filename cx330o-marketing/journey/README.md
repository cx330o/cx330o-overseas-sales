# cx330o Journey Builder

Customer journey automation module for the cx330o Sales Platform.

## Features

- Visual journey builder with drag-and-drop interface
- Omnichannel messaging (email, SMS, push, WhatsApp, Slack)
- User segmentation with multiple operators
- Broadcast campaigns
- Template editor (HTML/MJML and low-code)
- Event-based trigger automation
- Performance analytics dashboard

## Usage

```bash
# Part of the full platform
docker compose up -d
# Access at http://localhost:3010 (standalone) or via Marketing Gateway
```

## Architecture

Runs as a containerized service. Uses PostgreSQL for data storage and ClickHouse for analytics.
Integrates with the cx330o Marketing Gateway for unified API access.

## License

MIT — See root LICENSE file.
