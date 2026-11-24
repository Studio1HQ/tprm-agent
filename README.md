<div align="center">

<img src="https://raw.githubusercontent.com/Studio1HQ/Studio1HQ/main/assets/banners/tprm-agent.webp" alt="Vendor Risk Agent with Bright Data: Automated adverse media checks on vendors with SERP API and Web Unlocker" width="100%" />

<br />
<br />

# Vendor Risk Agent with Bright Data

### Automated adverse media checks on vendors with SERP API and Web Unlocker

A FastAPI service that searches for vendor red flags with the Bright Data SERP API, reads pages through Web Unlocker, scores risk with OpenAI, and generates monitoring scripts with the OpenHands SDK.

<br />

[![Built by Studio1](https://img.shields.io/badge/Built_by_Studio1-f97316?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNjAgMTYwIiBmaWxsPSJub25lIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTAgMzVDMCAxNi42ODA3IDE0LjA3NDQgMS42NDg0NCAzMiAwLjEyNjk1M1YxNDFINTEuMDUyM0M1Mi40MzA4IDEzNy4zNDQgNTQuNzQ0NiAxMzMuNjg5IDU3Ljk5MzggMTMwLjAzM0M2MS4xNDQ2IDEyNi41MDggNjQuNjg5MiAxMjMuNDQgNjguNjI3NyAxMjAuODI5QzcyLjU2NjIgMTE4LjM0OSA3Ni4zNTY5IDExNi43ODIgODAgMTE2LjEyOVY4Ni43NTQ0Qzc1LjQ3MDggODcuOTI5MiA3MS4zODQ2IDg5LjY5MTkgNjcuNzQxNSA5Mi4wNDE1QzY0IDk0LjUyMjUgNjAuNzUwOCA5Ny40NiA1Ny45OTM4IDEwMC44NTRDNTYuNTM0NSAxMDIuNzIgNTUuMjU0NSAxMDQuNjU5IDU0LjE1MzkgMTA2LjY3MVYwSDEyNUMxNDQuMzMgMCAxNjAgMTUuNjY5OSAxNjAgMzVWMTI1QzE2MCAxNDQuMzMgMTQ0LjMzIDE2MCAxMjUgMTYwSDEyNFYxOEgxMDQuOTQ4QzEwMy41NjkgMjEuNjgxNiAxMDEuMjU1IDI1LjM2MjggOTguMDA2MiAyOS4wNDQ0Qzk0Ljg1NTQgMzIuNTk0MiA5MS4zMTA4IDM1LjY4NDEgODcuMzcyMyAzOC4zMTRDODMuNDMzOCA0MC44MTIgNzkuNjQzMSA0Mi4zODk2IDc2IDQzLjA0NzRWNzIuNjMwNEM4MC41MjkyIDcxLjQ0NzMgODQuNjE1NCA2OS42NzI0IDg4LjI1ODUgNjcuMzA1N0M5MiA2NC44MDc2IDk1LjI0OTIgNjEuODQ5MSA5OC4wMDYyIDU4LjQzMDdDOTkuNDY1NSA1Ni41NTEzIDEwMC43NDUgNTQuNTk4NiAxMDEuODQ2IDUyLjU3MjNWMTYwSDM1QzE1LjY3IDE2MCAwIDE0NC4zMyAwIDEyNVYzNVoiIGZpbGw9IiNmZmZmZmYiLz48L3N2Zz4K)](https://studio1hq.com)
[![Built with Bright Data](https://img.shields.io/badge/Built_with_Bright_Data-141414?style=for-the-badge)](https://brightdata.com)

[Bright Data docs](https://docs.brightdata.com) &nbsp;·&nbsp; [Bright Data](https://brightdata.com) &nbsp;·&nbsp; [More examples](https://github.com/Studio1HQ) &nbsp;·&nbsp; [studio1hq.com](https://studio1hq.com)

</div>

<br />

## Overview

An agent for third-party risk management. Give it a vendor name and it searches for adverse media, reads the pages it finds, scores the risk, and can generate monitoring scripts that keep checking the vendor's sources.

It uses three Bright Data products: the SERP API to search Google for red flags, Web Unlocker to read pages behind paywalls and CAPTCHAs, and an optional Browser API for JavaScript-heavy sites. OpenAI scores the risk, and the OpenHands SDK writes the monitoring scripts. A FastAPI service exposes it over REST.

## Features

- **Adverse media search**: Litigation, fraud, financial, regulatory and operational risk categories.
- **SERP API discovery**: Searches Google for red flags per category.
- **Web Unlocker access**: Extracts content from protected pages.
- **AI risk analysis**: OpenAI returns severity (low, medium, high, critical), findings and recommended actions.
- **Generated monitors**: OpenHands SDK writes Python scripts into `scripts/generated/`.
- **REST API**: FastAPI endpoints with interactive docs.
- **Browser API (optional)**: Form filling and extraction for complex sites.

## Tech stack

| Layer | Tool |
| --- | --- |
| Search | [Bright Data SERP API](https://docs.brightdata.com/scraping-automation/serp-api/introduction) |
| Page access | [Bright Data Web Unlocker](https://docs.brightdata.com/scraping-automation/web-unlocker/introduction) |
| Browser (optional) | [Bright Data Browser API](https://docs.brightdata.com/scraping-automation/scraping-browser/introduction) with Playwright |
| Risk analysis | [OpenAI](https://platform.openai.com/docs) |
| Script generation | [OpenHands SDK](https://docs.openhands.dev/sdk/getting-started) |
| API | [FastAPI](https://fastapi.tiangolo.com) |
| Deployment | Railway (`Procfile`) |

## Getting started

### Prerequisites

- Python 3.12 or higher
- A [Bright Data](https://brightdata.com) account with API access
- An [OpenAI API key](https://platform.openai.com/api-keys)
- An [OpenHands Cloud](https://openhands.dev) account or your own LLM API key

### Installation

```bash
git clone https://github.com/Studio1HQ/tprm-agent.git
cd tprm-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root.

| Variable | Description |
| --- | --- |
| `BRIGHT_DATA_API_TOKEN` | Bright Data API token. |
| `BRIGHT_DATA_SERP_ZONE` | SERP API zone name. |
| `BRIGHT_DATA_UNLOCKER_ZONE` | Web Unlocker zone name. |
| `BRIGHT_DATA_CUSTOMER_ID` | Customer ID for Web Unlocker (in `config.py`). |
| `BRIGHT_DATA_UNLOCKER_PASSWORD` | Web Unlocker zone password (in `config.py`). |
| `BRIGHT_DATA_BROWSER_USER` | Optional. Browser API username. |
| `BRIGHT_DATA_BROWSER_PASSWORD` | Optional. Browser API password. |
| `OPENAI_API_KEY` | OpenAI key for risk analysis. |
| `LLM_API_KEY` | API key for OpenHands script generation. |
| `LLM_MODEL` | Model for OpenHands, for example `openai/gpt-4o`. |

Zones are created in the Bright Data dashboard under Proxies and Scraping Infrastructure: add a SERP API zone, a Web Unlocker zone and, optionally, a Scraping Browser.

### Run

Start the API:

```bash
python -m uvicorn api.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs. To run one investigation directly:

```bash
python src/agent.py
```

## How it works

```text
DISCOVERY (SERP API) -> ACCESS (Web Unlocker) -> ACTION (OpenAI + OpenHands SDK)
  search Google          bypass paywalls          analyze risks
  for red flags          and CAPTCHAs             generate scripts
```

```text
tprm-agent/
├── src/
│   ├── config.py      # settings
│   ├── discovery.py   # SERP API
│   ├── access.py      # Web Unlocker
│   ├── actions.py     # OpenAI + OpenHands SDK
│   ├── agent.py       # orchestration
│   └── browser.py     # Browser API (optional)
├── api/main.py        # FastAPI endpoints
├── scripts/generated/ # generated monitors
├── run_investigation.py
└── Procfile
```

Risk categories live in `RISK_CATEGORIES` in `src/discovery.py`; add your own keywords there.

### API

Start an investigation:

```bash
curl -X POST "http://localhost:8000/investigate" \
  -H "Content-Type: application/json" \
  -d '{"vendor_name": "Acme Corp", "categories": ["litigation", "fraud"], "generate_monitors": true}'
```

Other endpoints: `GET /investigate/{investigation_id}` for results, `GET /reports/{vendor_name}`, and `GET /health`.

Request fields: `vendor_name` (required), `categories` (optional), `generate_monitors` (optional, default true). A result includes `total_sources_found`, `total_sources_accessed`, `risk_assessments` (category, severity, summary, key findings, sources, recommended actions), `monitoring_scripts` and `errors`.

Python use:

```python
from src.agent import TPRMAgent

agent = TPRMAgent()
result = agent.investigate(
    vendor_name="Acme Corp",
    categories=["litigation", "financial", "fraud"],
    generate_monitors=True,
)
```

Run or schedule a generated monitor:

```bash
cd scripts/generated
python monitor_acme_corp.py
# cron: 0 9 * * * cd /path/to/tprm-agent/scripts/generated && python3 monitor_acme_corp.py
```

### Deploy to Railway

```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

Add the environment variables in the Railway dashboard under Variables, then generate a domain. The `Procfile` runs `uvicorn api.main:app --host 0.0.0.0 --port $PORT`.

### Troubleshooting

- **Bright Data auth errors**: Check the token and zone names, zone status and available bandwidth.
- **OpenAI rate limits**: Add retries or reduce concurrency.
- **Generated scripts skip Bright Data**: Check the Web Unlocker instructions in the prompt in `actions.py`.
- **Deployment failures**: Check dependency size and the `Procfile`.

Security: do not commit `.env`, use platform variables in production, rotate keys, and add authentication to the API before exposing it.

## Resources

- [Bright Data SERP API docs](https://docs.brightdata.com/scraping-automation/serp-api/introduction): Search zone setup.
- [Bright Data Web Unlocker docs](https://docs.brightdata.com/scraping-automation/web-unlocker/introduction): Unlocker zone setup.
- [Bright Data Browser API docs](https://docs.brightdata.com/scraping-automation/scraping-browser/introduction): Scraping Browser.
- [OpenHands SDK docs](https://docs.openhands.dev/sdk/getting-started): Agent SDK.
- [Bright Data](https://brightdata.com): Account and API token.

<br />

---

<div align="center">

<a href="https://studio1hq.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Studio1HQ/website/main/brand/studio1-logo-on-dark.svg" />
    <img src="https://raw.githubusercontent.com/Studio1HQ/website/main/brand/studio1-logo-on-light.svg" alt="Studio1" width="160" />
  </picture>
</a>

Built by **[Studio1](https://studio1hq.com)**, the technical content and DevRel partner for devtool teams. Made with [Bright Data](https://brightdata.com).<br />
Browse more open-source examples at [github.com/Studio1HQ](https://github.com/Studio1HQ).

[![Website](https://img.shields.io/badge/studio1hq.com-0b0807?style=for-the-badge&logo=googlechrome&logoColor=white)](https://studio1hq.com)
[![Book a call](https://img.shields.io/badge/Book_a_strategy_call-f97316?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://cal.com/studio1/collab)
[![X](https://img.shields.io/badge/%40Studio1HQ-141414?style=for-the-badge&logo=x&logoColor=white)](https://x.com/Studio1HQ)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/studio1hq/)

<sub><a href="https://studio1hq.com">studio1hq.com</a> · Technical content, docs, video and DevRel for devtools</sub>

</div>
