# cx330o Overseas Sales Platform

An AI-powered full-stack system for overseas sales automation — from lead generation to payment collection and customer success.

## System Architecture

```
cx330o-dashboard (:80) → Unified Login + PWA + GDPR Consent
    │
    ├── cx330o-infra/core
    │   ├── FlowEngine → Workflow Orchestration (400+ integrations)
    │   └── Analytics  → Data Dashboards (AI-powered BI)
    │
    ├── cx330o-leadgen/core   → Multi-source Lead Scraping
    ├── cx330o-outreach/core  → AI Cold Email + Voice Pipeline
    ├── cx330o-contracts/     → E-Signature (DocuSeal)          ← NEW
    ├── cx330o-payments/      → Payment Gateway (Hyperswitch)   ← NEW
    ├── cx330o-crm/core       → Customer Management (Twenty CRM)
    ├── cx330o-marketing/core → Omnichannel Marketing + Page Builder
    ├── cx330o-experiments/   → A/B Testing (GrowthBook)        ← NEW
    ├── cx330o-voip/          → Video Calls + AI Voice Agent    ← NEW
    ├── cx330o-privacy/       → GDPR/CCPA Compliance (Klaro)   ← NEW
    ├── cx330o-i18n/          → 50+ Languages + 135 Currencies  ← NEW
    └── cx330o-plugins/       → Social CRM (WhatsApp/IG/TG/LINE)
```

## Full Sales Cycle

1. **cx330o-leadgen** scrapes business data (Google Maps / Yelp / OSINT)
2. FlowEngine pushes new leads to **cx330o-outreach**
3. **cx330o-outreach** researches, scores, generates personalized emails + AI voice calls
4. Interested leads receive contracts via **cx330o-contracts** (DocuSeal)
5. Signed contracts trigger payment via **cx330o-payments** (Hyperswitch, 50+ processors)
6. Paid customers enter **cx330o-crm** for lifecycle management
7. CRM customers enter **cx330o-marketing** for ongoing engagement + A/B tested campaigns
8. Support handled by helpdesk with SLA tracking
9. All data flows into **Analytics** for dashboards

## Quick Start

```bash
# Core services only
docker compose up -d

# Full deployment (all modules)
docker compose --profile all up -d

# Or pick specific profiles
docker compose --profile marketing --profile contracts --profile payments up -d
```

```bash
# Wait ~60 seconds for all services to initialize, then open:
# http://localhost        → Dashboard (login: admin / abc123)
# http://localhost:81     → FlowEngine (workflow builder)
# http://localhost:82     → Analytics (BI dashboards)
# http://localhost:83     → CRM (customer management)
# http://localhost:84     → Contracts (e-signature)
# http://localhost:85     → Payments (control center)
# http://localhost:86     → Experiments (A/B testing)
# http://localhost:87     → VoIP (video conferencing)
```

```bash
# Or run the Python demo (no Docker needed)
pip install -r "cx330o-leadgen/core/requirements.txt"
pip install -r "cx330o-outreach/core/requirements.txt"
python demo_full.py
```

## Tech Stack

- **AI/Backend**: Python, LangChain, LangGraph, Groq, OpenAI
- **Frontend**: Next.js 15, TypeScript, React 19, Tailwind CSS
- **Infrastructure**: Docker, Nginx, PostgreSQL, MongoDB, Redis
- **Workflow**: Custom FlowEngine (400+ integrations)
- **Analytics**: Built-in BI Dashboard (Metabase)
- **CRM**: Full-featured CRM Platform (Twenty CRM)
- **Marketing**: Journey Builder, High-performance Mailer, Live Chat, Page Builder (GrapesJS)
- **Payments**: Unified Payment Gateway (Hyperswitch, Rust, 50+ processors)
- **Contracts**: E-Signature Platform (DocuSeal)
- **Experiments**: A/B Testing + Feature Flags (GrowthBook)
- **VoIP**: Video Conferencing (MiroTalk WebRTC) + AI Voice Agent (Bolna)
- **Privacy**: GDPR/CCPA Consent Management (Klaro.js)
- **i18n**: 50+ Languages, 135+ Currencies (i18next)

## Modules

| Module | Path | Description | Tech |
|--------|------|-------------|------|
| LeadGen | `cx330o-leadgen/` | Multi-source lead scraping with AI enrichment | Python, Playwright, Groq |
| Outreach | `cx330o-outreach/` | AI-powered sales outreach pipeline | Python, LangChain, SMTP |
| Contracts | `cx330o-contracts/` | E-signature & document signing | Ruby/Rails, PostgreSQL |
| Payments | `cx330o-payments/` | Unified payment gateway (50+ processors) | Rust, PostgreSQL, Redis |
| CRM | `cx330o-crm/` | Customer management with PDF and email extensions | Node.js, PostgreSQL |
| Marketing | `cx330o-marketing/` | Unified marketing gateway with page builder | Node.js, Express, Go |
| Experiments | `cx330o-experiments/` | A/B testing & feature flags | Node.js, MongoDB |
| VoIP | `cx330o-voip/` | Video conferencing + AI voice agent | Node.js, Python, WebRTC |
| Privacy | `cx330o-privacy/` | GDPR/CCPA compliance suite | JavaScript, Python |
| i18n | `cx330o-i18n/` | Multi-language + multi-currency framework | JavaScript, i18next |
| Infra | `cx330o-infra/` | Workflow orchestration and analytics | PostgreSQL, Docker |
| Dashboard | `cx330o-dashboard/` | Unified login portal with SSO + PWA | Express, Nginx |
| Plugins | `cx330o-plugins/` | Social CRM for 4 platforms | Next.js, TypeScript |
| Extensions | `cx330o-extensions/` | ERP & HR modules | Python, Node.js |

## Docker Compose Profiles

| Profile | What it adds |
|---------|-------------|
| (default) | Dashboard, FlowEngine, Analytics, CRM, PDF Generator, Email Parser |
| `marketing` | Journey Builder, Mailer, Live Chat, Lead Scoring |
| `contracts` | DocuSeal (e-signature) |
| `payments` | Hyperswitch (payment gateway + control center) |
| `experiments` | GrowthBook (A/B testing + feature flags) |
| `voip` | MiroTalk (video) + Bolna (AI voice) |
| `all` | Everything |

## Project Structure

```
cx330o-overseas-sales/
├── cx330o-leadgen/          # Lead generation & scraping
│   ├── core/                # Main pipeline
│   ├── harvester/           # OSINT intelligence engine
│   ├── maps-scraper/        # Google Maps scraper
│   ├── web-scraper/         # Playwright web scraper
│   └── enricher/            # AI data enrichment
├── cx330o-outreach/         # AI cold outreach
│   ├── core/                # Main pipeline
│   ├── sales-agent/         # 8-stage conversational AI
│   ├── email-automations/   # Multi-agent email system
│   ├── email-manager/       # Template & scheduling
│   ├── email-generator/     # Fast LLM email generation
│   └── workflow/            # LangGraph state machine
├── cx330o-contracts/        # E-signature (DocuSeal)        ← NEW
├── cx330o-payments/         # Payment gateway (Hyperswitch)  ← NEW
├── cx330o-crm/              # Customer relationship management
│   ├── core/                # CRM deployment + extensions
│   ├── platform/            # Full CRM platform
│   ├── erp-extensions/      # ERP features (invoicing, PDF)
│   └── email-crm/           # Email parsing & webhook
├── cx330o-marketing/        # Marketing automation
│   ├── core/                # API gateway
│   ├── journey/             # Customer journey builder
│   ├── mailer/              # Email delivery engine
│   ├── chat/                # Omnichannel live chat
│   ├── scoring/             # Lead scoring engine
│   └── page-builder/        # GrapesJS page builder          ← NEW
├── cx330o-experiments/      # A/B testing (GrowthBook)       ← NEW
├── cx330o-voip/             # Video + AI voice               ← NEW
│   ├── mirotalk/            # WebRTC video conferencing
│   └── bolna/               # AI voice agent
├── cx330o-privacy/          # GDPR/CCPA compliance           ← NEW
├── cx330o-i18n/             # Multi-language + multi-currency ← NEW
│   └── locales/             # Language packs (en/zh/ja/es/ar)
├── cx330o-infra/            # Infrastructure
│   ├── core/                # Docker deployment
│   ├── workflow-engine/     # Visual workflow builder
│   └── analytics/           # BI dashboards
├── cx330o-dashboard/        # Unified login portal + PWA
├── cx330o-plugins/          # Social CRM plugins
│   ├── whatsapp-crm/
│   ├── instagram-crm/
│   ├── telegram-crm/
│   └── line-crm/
├── cx330o-extensions/       # ERP & HR modules
├── others/                  # Source packages (reference)
├── demo_full.py             # End-to-end demo script
└── docker-compose.yml       # Unified orchestration
```

## License

MIT
