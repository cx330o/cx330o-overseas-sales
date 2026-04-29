# cx330o MailRadar

Inbound email parsing and CRM integration module for the cx330o Sales Platform.

## Features

- Inbound email parsing via webhook
- Contact extraction from email headers and body
- Automatic CRM synchronization
- Email thread tracking
- Custom attribute mapping
- Sendgrid webhook support

## Usage

```bash
# Part of the full platform
docker compose up -d
# API available at http://localhost:3003
```

## Architecture

Built with Laravel (PHP). Parses incoming emails and syncs extracted contact data to the CRM.

## License

MIT — See root LICENSE file.
