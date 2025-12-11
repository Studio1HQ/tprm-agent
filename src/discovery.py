import requests
from typing import Optional
from dataclasses import dataclass
from urllib.parse import quote_plus
from config import settings


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str


class DiscoveryClient:
    """Search for adverse media using Bright Data SERP API (Direct API)."""

    RISK_CATEGORIES = {
        "litigation": ["lawsuit", "litigation", "sued", "court case", "legal action"],
        "financial": ["bankruptcy", "insolvency", "debt", "financial trouble", "default"],
        "fraud": ["fraud", "scam", "investigation", "indictment", "scandal"],
        "regulatory": ["violation", "fine", "penalty", "sanctions", "compliance"],
        "operational": ["recall", "safety issue", "supply chain", "disruption"],
    }

    def __init__(self):
        self.api_url = "https://api.brightdata.com/request"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BRIGHT_DATA_API_TOKEN}",
        }

    def _build_queries(self, vendor_name: str, categories: Optional[list] = None) -> list[str]:
        """Build search queries for each risk category."""
        categories = categories or list(self.RISK_CATEGORIES.keys())
        queries = []

        for category in categories:
            keywords = self.RISK_CATEGORIES.get(category, [])
            keyword_str = " OR ".join(keywords)
            query = f'"{vendor_name}" ({keyword_str})'
            queries.append(query)

        return queries

    def search(self, query: str) -> list[SearchResult]:
        """Execute a single search query using Bright Data SERP API."""
        try:
            # Build Google search URL with brd_json=1 for parsed JSON
            encoded_query = quote_plus(query)
            google_url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us&brd_json=1"

            payload = {
                "zone": settings.BRIGHT_DATA_SERP_ZONE,
                "url": google_url,
                "format": "raw",
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            organic = data.get("organic", [])

            for item in organic:
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=item.get("description", ""),
                        source=item.get("displayed_link", ""),
                    )
                )
            return results

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def discover_adverse_media(
        self,
        vendor_name: str,
        categories: Optional[list] = None,
    ) -> dict[str, list[SearchResult]]:
        """Search for adverse media across all risk categories."""
        queries = self._build_queries(vendor_name, categories)
        category_names = categories or list(self.RISK_CATEGORIES.keys())

        categorized_results = {}
        for category, query in zip(category_names, queries):
            print(f"  Searching: {category}...")
            results = self.search(query)
            categorized_results[category] = results

        return categorized_results

    def filter_relevant_results(
        self, results: dict[str, list[SearchResult]], vendor_name: str
    ) -> dict[str, list[SearchResult]]:
        """Filter out irrelevant results."""
        filtered = {}
        vendor_lower = vendor_name.lower()

        for category, items in results.items():
            relevant = []
            for item in items:
                if (
                    vendor_lower in item.title.lower()
                    or vendor_lower in item.snippet.lower()
                ):
                    relevant.append(item)
            filtered[category] = relevant

        return filtered