import asyncio
from playwright.async_api import async_playwright, Playwright
from dataclasses import dataclass
from typing import Optional
from config import settings


@dataclass
class BrowserContent:
    url: str
    title: str
    text: str
    screenshot_path: Optional[str]
    success: bool
    error: Optional[str] = None


class BrowserClient:
    """Access dynamic content using Bright Data Browser API (Scraping Browser).
    
    Use this for:
    - JavaScript-heavy sites that require full rendering
    - Multi-step forms (e.g., court registry searches)
    - Sites requiring clicks, scrolling, or interaction
    - Capturing screenshots for compliance documentation
    """

    def __init__(self):
        # Build WebSocket endpoint for CDP connection
        auth = f"{settings.BRIGHT_DATA_BROWSER_USER}:{settings.BRIGHT_DATA_BROWSER_PASSWORD}"
        self.endpoint_url = f"wss://{auth}@brd.superproxy.io:9222"

    async def fetch_dynamic_page(
        self,
        url: str,
        wait_for_selector: Optional[str] = None,
        take_screenshot: bool = False,
        screenshot_path: Optional[str] = None,
    ) -> BrowserContent:
        """Fetch content from a dynamic page using Browser API."""
        async with async_playwright() as playwright:
            try:
                print(f"Connecting to Bright Data Scraping Browser...")
                browser = await playwright.chromium.connect_over_cdp(self.endpoint_url)

                try:
                    page = await browser.new_page()
                    print(f"Navigating to {url}...")
                    await page.goto(url, timeout=120000)

                    # Wait for specific selector if provided
                    if wait_for_selector:
                        await page.wait_for_selector(wait_for_selector, timeout=30000)

                    # Get page content
                    title = await page.title()
                    content = await page.content()

                    # Extract text
                    text = await page.evaluate("() => document.body.innerText")

                    # Take screenshot if requested
                    if take_screenshot and screenshot_path:
                        await page.screenshot(path=screenshot_path, full_page=True)

                    return BrowserContent(
                        url=url,
                        title=title,
                        text=text[:10000],
                        screenshot_path=screenshot_path if take_screenshot else None,
                        success=True,
                    )

                finally:
                    await browser.close()

            except Exception as e:
                return BrowserContent(
                    url=url,
                    title="",
                    text="",
                    screenshot_path=None,
                    success=False,
                    error=str(e),
                )

    async def fill_and_submit_form(
        self,
        url: str,
        form_data: dict[str, str],
        submit_selector: str,
        result_selector: str,
    ) -> BrowserContent:
        """Fill a form and get results - useful for court registries."""
        async with async_playwright() as playwright:
            try:
                browser = await playwright.chromium.connect_over_cdp(self.endpoint_url)

                try:
                    page = await browser.new_page()
                    await page.goto(url, timeout=120000)

                    # Fill form fields
                    for selector, value in form_data.items():
                        await page.fill(selector, value)

                    # Submit form
                    await page.click(submit_selector)

                    # Wait for results
                    await page.wait_for_selector(result_selector, timeout=30000)

                    title = await page.title()
                    text = await page.evaluate("() => document.body.innerText")

                    return BrowserContent(
                        url=url,
                        title=title,
                        text=text[:10000],
                        screenshot_path=None,
                        success=True,
                    )

                finally:
                    await browser.close()

            except Exception as e:
                return BrowserContent(
                    url=url,
                    title="",
                    text="",
                    screenshot_path=None,
                    success=False,
                    error=str(e),
                )

    async def scroll_and_collect(
        self,
        url: str,
        scroll_count: int = 5,
        wait_between_scrolls: float = 1.0,
    ) -> BrowserContent:
        """Handle infinite scroll pages."""
        async with async_playwright() as playwright:
            try:
                browser = await playwright.chromium.connect_over_cdp(self.endpoint_url)

                try:
                    page = await browser.new_page()
                    await page.goto(url, timeout=120000)

                    # Scroll down multiple times
                    for i in range(scroll_count):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await asyncio.sleep(wait_between_scrolls)

                    title = await page.title()
                    text = await page.evaluate("() => document.body.innerText")

                    return BrowserContent(
                        url=url,
                        title=title,
                        text=text[:10000],
                        screenshot_path=None,
                        success=True,
                    )

                finally:
                    await browser.close()

            except Exception as e:
                return BrowserContent(
                    url=url,
                    title="",
                    text="",
                    screenshot_path=None,
                    success=False,
                    error=str(e),
                )


# Example usage for court registry search
async def example_court_search():
    client = BrowserClient()

    # Example: Search a court registry
    result = await client.fill_and_submit_form(
        url="https://example-court-registry.gov/search",
        form_data={
            "#party-name": "Acme Corp",
            "#case-type": "civil",
        },
        submit_selector="#search-button",
        result_selector=".search-results",
    )

    if result.success:
        print(f"Found court records: {result.text[:500]}")
    else:
        print(f"Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(example_court_search())