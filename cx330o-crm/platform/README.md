# cx330o CRM Platform

Modern customer relationship management system for the cx330o Sales Platform.

## Features

- Full customer lifecycle management
- Customizable objects and fields
- Kanban, table, and filter views
- Email integration and activity tracking
- REST API for external integrations
- Extensible app system

## Usage

CRM is deployed as part of the cx330o platform via Docker Compose.

```bash
# Full platform
docker compose up -d
# Access at http://localhost:83
```

## Architecture

CRM runs on port 3000 internally, exposed via Nginx on port 83.
Data is stored in PostgreSQL with Redis for caching.

## License

See root LICENSE file.
