import os
import json
from datetime import datetime, UTC
from dataclasses import dataclass, asdict
from openai import OpenAI
from pydantic import SecretStr
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from config import settings


@dataclass
class RiskAssessment:
    vendor_name: str
    category: str
    severity: str
    summary: str
    key_findings: list[str]
    sources: list[str]
    recommended_actions: list[str]
    assessed_at: str


@dataclass
class MonitoringScript:
    vendor_name: str
    script_path: str
    urls_monitored: list[str]
    check_frequency: str
    created_at: str


class ActionsClient:
    """Analyze risks using OpenAI and generate monitoring scripts using OpenHands SDK."""

    def __init__(self):
        # OpenAI for risk analysis
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # OpenHands for agentic script generation
        self.llm = LLM(
            model=settings.LLM_MODEL,
            api_key=SecretStr(settings.LLM_API_KEY),
        )
        
        self.workspace = os.path.join(os.getcwd(), "scripts", "generated")
        os.makedirs(self.workspace, exist_ok=True)

    def analyze_risk(
        self,
        vendor_name: str,
        category: str,
        content: list[dict],
    ) -> RiskAssessment:
        """Analyze extracted content for risk severity using OpenAI."""
        content_summary = "\n\n".join(
            [f"Source: {c['url']}\nTitle: {c['title']}\nContent: {c['text'][:2000]}" for c in content]
        )

        prompt = f"""Analyze the following content about "{vendor_name}" for third-party risk assessment.

Category: {category}

Content:
{content_summary}

Provide a JSON response with:
{{
    "severity": "low|medium|high|critical",
    "summary": "2-3 sentence summary of findings",
    "key_findings": ["finding 1", "finding 2", ...],
    "recommended_actions": ["action 1", "action 2", ...]
}}

Consider:
- Severity should be based on potential business impact
- Critical = immediate action required (active fraud, bankruptcy filing)
- High = significant risk requiring investigation
- Medium = notable concern worth monitoring
- Low = minor issue or historical matter
"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        response_text = response.choices[0].message.content
        try:
            result = json.loads(response_text)
        except (json.JSONDecodeError, ValueError):
            result = {
                "severity": "medium",
                "summary": "Unable to parse risk assessment",
                "key_findings": [],
                "recommended_actions": ["Manual review required"],
            }

        return RiskAssessment(
            vendor_name=vendor_name,
            category=category,
            severity=result.get("severity", "medium"),
            summary=result.get("summary", ""),
            key_findings=result.get("key_findings", []),
            sources=[c["url"] for c in content],
            recommended_actions=result.get("recommended_actions", []),
            assessed_at=datetime.now(UTC).isoformat(),
        )

    def generate_monitoring_script(
        self,
        vendor_name: str,
        urls: list[str],
        check_keywords: list[str],
    ) -> MonitoringScript:
        """Generate a Python monitoring script using OpenHands SDK agent."""
        script_name = f"monitor_{vendor_name.lower().replace(' ', '_')}.py"
        script_path = os.path.join(self.workspace, script_name)

        prompt = f"""Create a Python monitoring script at {script_path} that:

1. Checks these URLs daily for new content: {urls[:5]}
2. Looks for these keywords: {check_keywords}
3. Sends an alert (print to console) if new relevant content is found
4. Logs all checks to a JSON file named 'monitoring_log.json'

The script MUST use Bright Data Web Unlocker API to bypass paywalls and CAPTCHAs:
- API endpoint: https://api.brightdata.com/request
- Use environment variable BRIGHT_DATA_API_TOKEN for the Bearer token
- Use environment variable BRIGHT_DATA_UNLOCKER_ZONE for the zone name
- Make POST requests with JSON payload: {{"zone": "zone_name", "url": "target_url", "format": "raw"}}
- Add header: "Authorization": "Bearer <token>"
- Add header: "Content-Type": "application/json"

The script should:
- Load Bright Data credentials from environment variables using python-dotenv
- Use the Bright Data Web Unlocker API for all HTTP requests (NOT plain requests.get)
- Handle errors gracefully with try/except
- Include a main() function that can be run directly
- Support being scheduled via cron
- Store content hashes to detect changes

Write the complete script to {script_path}.
"""

        # Create OpenHands agent with terminal and file editor tools
        agent = Agent(
            llm=self.llm,
            tools=[
                Tool(name=TerminalTool.name),
                Tool(name=FileEditorTool.name),
            ],
        )

        # Run the agent to generate the script
        conversation = Conversation(agent=agent, workspace=self.workspace)
        conversation.send_message(prompt)
        conversation.run()

        return MonitoringScript(
            vendor_name=vendor_name,
            script_path=script_path,
            urls_monitored=urls[:5],
            check_frequency="daily",
            created_at=datetime.now(UTC).isoformat(),
        )

    def export_assessment(self, assessment: RiskAssessment, output_path: str) -> None:
        """Export risk assessment to JSON file."""
        with open(output_path, "w") as f:
            json.dump(asdict(assessment), f, indent=2)