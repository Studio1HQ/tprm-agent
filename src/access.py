import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
from config import settings


@dataclass
class ExtractedContent:
    url: str
    title: str
    text: str
    publish_date: Optional[str]
    author: Optional[str]
    success: bool
    error: Optional[str] = None


class AccessClient:
    """Access protected content using Bright Data Web Unlocker (API-based)."""

    def __init__(self):
        self.api_url = "https://api.brightdata.com/request"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BRIGHT_DATA_API_TOKEN}",
        }

    def fetch_url(self, url: str) -> ExtractedContent:
        """Fetch and extract content from a URL using Web Unlocker API."""
        try:
            payload = {
                "zone": settings.BRIGHT_DATA_UNLOCKER_ZONE,
                "url": url,
                "format": "raw",
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()

            # Web Unlocker API returns the HTML directly
            html_content = response.text
            content = self._extract_content(html_content, url)
            return content

        except requests.Timeout:
            return ExtractedContent(
                url=url,
                title="",
                text="",
                publish_date=None,
                author=None,
                success=False,
                error="Request timed out",
            )
        except Exception as e:
            return ExtractedContent(
                url=url,
                title="",
                text="",
                publish_date=None,
                author=None,
                success=False,
                error=str(e),
            )

    def _extract_content(self, html: str, url: str) -> ExtractedContent:
        """Extract article content from HTML."""
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)

        # Extract main content
        article = soup.find("article") or soup.find("main") or soup.find("body")
        text = article.get_text(separator="\n", strip=True) if article else ""

        # Limit text length
        text = text[:10000] if len(text) > 10000 else text

        # Try to extract publish date
        publish_date = None
        date_meta = soup.find("meta", {"property": "article:published_time"})
        if date_meta:
            publish_date = date_meta.get("content")

        # Try to extract author
        author = None
        author_meta = soup.find("meta", {"name": "author"})
        if author_meta:
            author = author_meta.get("content")

        return ExtractedContent(
            url=url,
            title=title,
            text=text,
            publish_date=publish_date,
            author=author,
            success=True,
        )

    def fetch_multiple(self, urls: list[str]) -> list[ExtractedContent]:
        """Fetch multiple URLs sequentially."""
        results = []
        for url in urls:
            print(f"  Fetching: {url[:60]}...")
            content = self.fetch_url(url)
            if not content.success:
                print(f"  Error: {content.error}")
            results.append(content)
        return results