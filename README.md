# TPRM Agent - Autonomous Third-Party Risk Management

An AI-powered agent that automates vendor adverse media investigations using Bright Data's web scraping infrastructure, OpenAI for risk analysis, and OpenHands SDK for intelligent monitoring script generation.

## Features

- **Automated Vendor Investigation**: Search for adverse media across multiple risk categories (litigation, fraud, financial issues, regulatory violations, operational risks)
- **Intelligent Web Scraping**: Uses Bright Data SERP API and Web Unlocker to bypass paywalls, CAPTCHAs, and access protected content
- **AI Risk Analysis**: OpenAI analyzes extracted content and provides severity scores with actionable recommendations
- **Auto-Generated Monitoring**: OpenHands SDK creates production-ready Python scripts that continuously monitor vendor sources
- **REST API**: FastAPI-based endpoints for easy integration into existing systems
- **Browser Automation**: Optional Bright Data Browser API support for JavaScript-heavy sites and complex workflows

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   DISCOVERY     │────▶│     ACCESS      │────▶│     ACTION      │
│   (SERP API)    │     │ (Web Unlocker)  │     │ (OpenAI + SDK)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Search Google          Bypass paywalls         Analyze risks
   for red flags          and CAPTCHAs           Generate scripts
```

## Prerequisites

- Python 3.12 or higher
- [Bright Data account](https://brightdata.com/) with API access
- [OpenAI API key](https://platform.openai.com/api-keys)
- [OpenHands Cloud account](https://openhands.dev/) or your own LLM API key

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd tprm-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Bright Data API Token (for SERP API)
BRIGHT_DATA_API_TOKEN=your_api_token

# Bright Data SERP Zone
BRIGHT_DATA_SERP_ZONE=your_serp_zone_name

# Bright Data Web Unlocker Zone
BRIGHT_DATA_UNLOCKER_ZONE=your_unlocker_zone_name

# OpenAI (for risk analysis)
OPENAI_API_KEY=your_openai_api_key

# OpenHands (for agentic script generation)
LLM_API_KEY=your_llm_api_key
LLM_MODEL=openai/gpt-4o
```

### 3. Run Locally

**Start the API server:**

```bash
python -m uvicorn api.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

**Run a direct investigation:**

```bash
python src/agent.py
```

## Usage

### API Endpoints

#### Start Investigation

```bash
curl -X POST "http://localhost:8000/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_name": "Acme Corp",
    "categories": ["litigation", "fraud"],
    "generate_monitors": true
  }'
```

Response:

```json
{
 "investigation_id": "uuid-here",
 "status": "started",
 "message": "Investigation started for Acme Corp"
}
```

#### Get Investigation Results

```bash
curl http://localhost:8000/investigate/{investigation_id}
```

#### Health Check

```bash
curl http://localhost:8000/health
```

### Python Usage

```python
from src.agent import TPRMAgent

# Initialize agent
agent = TPRMAgent()

# Run investigation
result = agent.investigate(
    vendor_name="Acme Corp",
    categories=["litigation", "financial", "fraud"],
    generate_monitors=True
)

# Print results
print(f"Found {result.total_sources_found} sources")
print(f"Risk Assessments: {len(result.risk_assessments)}")

for assessment in result.risk_assessments:
    print(f"\n[{assessment.category}] Severity: {assessment.severity}")
    print(f"Summary: {assessment.summary}")
```

## Project Structure

```
tprm-agent/
├── src/
│   ├── __init__.py
│   ├── config.py         # Configuration and settings
│   ├── discovery.py      # SERP API integration
│   ├── access.py         # Web Unlocker integration
│   ├── actions.py        # OpenAI + OpenHands SDK
│   ├── agent.py          # Main orchestration
│   └── browser.py        # Browser API (optional)
├── api/
│   └── main.py           # FastAPI endpoints
├── scripts/
│   └── generated/        # Auto-generated monitoring scripts
├── .env                  # Environment variables (not in git)
├── requirements.txt      # Python dependencies
├── Procfile             # Railway deployment config
└── README.md
```

## Deployment

### Deploy to Railway

1. **Install Railway CLI:**

```bash
npm i -g @railway/cli
```

2. **Login and initialize:**

```bash
railway login
railway init
```

3. **Deploy:**

```bash
railway up
```

4. **Add environment variables** in Railway dashboard → Variables

5. **Generate domain:**

```bash
railway domain
```

### Deploy to Render

1. **Create `render.yaml`** (already included)

2. **Push to GitHub**

3. **Connect to Render:**

   - Go to [render.com](https://render.com)
   - New → Web Service
   - Connect your repository
   - Render auto-detects configuration

4. **Add environment variables** in Render dashboard

## Monitoring Scripts

After investigation, auto-generated monitoring scripts are saved in `scripts/generated/`:

### Run Monitoring Script

```bash
cd scripts/generated
python monitor_acme_corp.py
```

### Schedule with Cron

```bash
crontab -e
```

Add:

```
0 9 * * * cd /path/to/tprm-agent/scripts/generated && python3 monitor_acme_corp.py
```

## Configuration

### Bright Data Setup

1. **SERP API Zone:**

   - Go to Bright Data dashboard → Proxies & Scraping Infrastructure
   - Add → SERP API
   - Copy zone name and API token

2. **Web Unlocker Zone:**

   - Add → Web Unlocker
   - Copy zone name

3. **Browser API (Optional):**
   - Add → Scraping Browser
   - Copy credentials for advanced scenarios

### Risk Categories

Modify `src/discovery.py` to add custom risk categories:

```python
RISK_CATEGORIES = {
    "litigation": ["lawsuit", "litigation", "sued"],
    "financial": ["bankruptcy", "insolvency", "debt"],
    "fraud": ["fraud", "scam", "investigation"],
    "regulatory": ["violation", "fine", "penalty"],
    "operational": ["recall", "safety issue", "disruption"],
    # Add your custom categories here
}
```

## API Reference

### Investigation Request

```json
{
  "vendor_name": "string (required)",
  "categories": ["litigation", "fraud"] (optional),
  "generate_monitors": true (optional, default: true)
}
```

### Investigation Result

```json
{
 "vendor_name": "string",
 "started_at": "ISO 8601 timestamp",
 "completed_at": "ISO 8601 timestamp",
 "total_sources_found": 0,
 "total_sources_accessed": 0,
 "risk_assessments": [
  {
   "vendor_name": "string",
   "category": "string",
   "severity": "low|medium|high|critical",
   "summary": "string",
   "key_findings": ["string"],
   "sources": ["url"],
   "recommended_actions": ["string"],
   "assessed_at": "ISO 8601 timestamp"
  }
 ],
 "monitoring_scripts": [
  {
   "vendor_name": "string",
   "script_path": "string",
   "urls_monitored": ["url"],
   "check_frequency": "daily",
   "created_at": "ISO 8601 timestamp"
  }
 ],
 "errors": ["string"]
}
```

## Advanced Features

### Using Browser API

For JavaScript-heavy sites or complex workflows:

```python
from src.browser import BrowserClient
import asyncio

async def search_court_registry():
    client = BrowserClient()

    result = await client.fill_and_submit_form(
        url="https://court-registry.example.com/search",
        form_data={
            "#party-name": "Acme Corp",
            "#case-type": "civil",
        },
        submit_selector="#search-button",
        result_selector=".search-results",
    )

    if result.success:
        print(f"Court records: {result.text}")

asyncio.run(search_court_registry())
```

## Troubleshooting

### Common Issues

**Authentication errors with Bright Data:**

- Verify API token and zone names in `.env`
- Check zone status in Bright Data dashboard
- Ensure zones have available bandwidth

**OpenAI rate limits:**

- Add retry logic or reduce concurrent requests
- Upgrade OpenAI plan for higher limits

**Generated scripts not using Bright Data:**

- Check that OpenHands SDK prompt includes Web Unlocker instructions
- Verify `actions.py` has the correct prompt template

**Deployment failures:**

- Check dependency sizes (Railway/Render support larger apps than Vercel)
- Verify `Procfile` exists and is correct
- Ensure all environment variables are set

## Performance Tips

- **Parallel requests:** Modify `access.py` to use `asyncio` for faster content extraction
- **Caching:** Implement Redis caching for repeated vendor investigations
- **Rate limiting:** Add rate limiting middleware to prevent API abuse
- **Database:** Use PostgreSQL to persist investigation history

## Security

- Never commit `.env` file to git
- Use Railway/Render environment variables for production
- Rotate API keys regularly
- Implement authentication on API endpoints for production use

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Resources

- [Bright Data SERP API Documentation](https://docs.brightdata.com/scraping-automation/serp-api/introduction)
- [Bright Data Web Unlocker Documentation](https://docs.brightdata.com/scraping-automation/web-unlocker/introduction)
- [Bright Data Browser API Documentation](https://docs.brightdata.com/scraping-automation/scraping-browser/introduction)
- [OpenHands SDK Documentation](https://docs.openhands.dev/sdk/getting-started)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Support

For issues and questions:

- Open an issue on GitHub
- Check Bright Data documentation
- Review OpenHands SDK examples

## Roadmap

- [ ] Add support for SEC filings and OFAC sanctions lists
- [ ] Implement PostgreSQL database for investigation history
- [ ] Add Slack/Teams webhook notifications
- [ ] Build React dashboard for visualization
- [ ] Support batch vendor investigations
- [ ] Add PDF report generation
- [ ] Implement user authentication
- [ ] Add multi-language support
