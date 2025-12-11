from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional

from discovery import DiscoveryClient, SearchResult
from access import AccessClient, ExtractedContent
from actions import ActionsClient, RiskAssessment, MonitoringScript


@dataclass
class InvestigationResult:
    vendor_name: str
    started_at: str
    completed_at: str
    total_sources_found: int
    total_sources_accessed: int
    risk_assessments: list[RiskAssessment]
    monitoring_scripts: list[MonitoringScript]
    errors: list[str]


class TPRMAgent:
    """Autonomous agent for Third-Party Risk Management investigations."""

    def __init__(self):
        self.discovery = DiscoveryClient()
        self.access = AccessClient()
        self.actions = ActionsClient()

    def investigate(
        self,
        vendor_name: str,
        categories: Optional[list[str]] = None,
        generate_monitors: bool = True,
    ) -> InvestigationResult:
        """Run a complete vendor investigation."""
        started_at = datetime.now(UTC).isoformat()
        errors = []
        risk_assessments = []
        monitoring_scripts = []

        # Stage 1: Discovery (SERP API)
        print(f"[Discovery] Searching for adverse media about {vendor_name}...")
        try:
            raw_results = self.discovery.discover_adverse_media(vendor_name, categories)
            filtered_results = self.discovery.filter_relevant_results(raw_results, vendor_name)
        except Exception as e:
            errors.append(f"Discovery failed: {str(e)}")
            return InvestigationResult(
                vendor_name=vendor_name,
                started_at=started_at,
                completed_at=datetime.now(UTC).isoformat(),
                total_sources_found=0,
                total_sources_accessed=0,
                risk_assessments=[],
                monitoring_scripts=[],
                errors=errors,
            )

        total_sources = sum(len(results) for results in filtered_results.values())
        print(f"[Discovery] Found {total_sources} relevant sources")

        # Stage 2: Access (Web Unlocker)
        print(f"[Access] Extracting content from sources...")
        all_urls = []
        url_to_category = {}
        for category, results in filtered_results.items():
            for result in results:
                all_urls.append(result.url)
                url_to_category[result.url] = category

        try:
            extracted_content = self.access.fetch_multiple(all_urls)
            successful_extractions = [c for c in extracted_content if c.success]
        except Exception as e:
            error_msg = f"Access failed: {str(e)}"
            print(f"[Access] {error_msg}")
            errors.append(error_msg)
            successful_extractions = []

        print(f"[Access] Successfully extracted {len(successful_extractions)} sources")

        # Stage 3: Action - Analyze risks (OpenAI)
        print(f"[Action] Analyzing risks...")
        category_content = {}
        for content in successful_extractions:
            category = url_to_category.get(content.url, "unknown")
            if category not in category_content:
                category_content[category] = []
            category_content[category].append({
                "url": content.url,
                "title": content.title,
                "text": content.text,
            })

        for category, content_list in category_content.items():
            if not content_list:
                continue
            try:
                assessment = self.actions.analyze_risk(vendor_name, category, content_list)
                risk_assessments.append(assessment)
            except Exception as e:
                errors.append(f"Risk analysis failed for {category}: {str(e)}")

        # Stage 3: Action - Generate monitoring scripts
        if generate_monitors and successful_extractions:
            print(f"[Action] Generating monitoring scripts...")
            try:
                urls_to_monitor = [c.url for c in successful_extractions[:10]]
                keywords = [vendor_name, "lawsuit", "bankruptcy", "fraud"]
                script = self.actions.generate_monitoring_script(
                    vendor_name, urls_to_monitor, keywords
                )
                monitoring_scripts.append(script)
            except Exception as e:
                errors.append(f"Script generation failed: {str(e)}")

        completed_at = datetime.now(UTC).isoformat()
        print(f"[Complete] Investigation finished")

        return InvestigationResult(
            vendor_name=vendor_name,
            started_at=started_at,
            completed_at=completed_at,
            total_sources_found=total_sources,
            total_sources_accessed=len(successful_extractions),
            risk_assessments=risk_assessments,
            monitoring_scripts=monitoring_scripts,
            errors=errors,
        )


def main():
    """Example usage."""
    agent = TPRMAgent()
    result = agent.investigate("Acme Corp")

    print(f"\n{'='*50}")
    print(f"Investigation Complete: {result.vendor_name}")
    print(f"Sources Found: {result.total_sources_found}")
    print(f"Sources Accessed: {result.total_sources_accessed}")
    print(f"Risk Assessments: {len(result.risk_assessments)}")
    print(f"Monitoring Scripts: {len(result.monitoring_scripts)}")

    for assessment in result.risk_assessments:
        print(f"\n[{assessment.category.upper()}] Severity: {assessment.severity}")
        print(f"Summary: {assessment.summary}")


if __name__ == "__main__":
    main()