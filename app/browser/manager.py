from playwright.async_api import async_playwright
from app.config.settings import settings
from app.utils.logger import logger


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self._page = None

    async def start(self):
        logger.info("Starting Browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=settings.HEADLESS
        )
        logger.info("Chromium Started")

    async def stop(self):
        logger.info("Stopping Browser...")
        if self._page and not self._page.is_closed():
            await self._page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self._page = None
        logger.info("Chromium Stopped")

    async def get_page(self):
        """Return the current page or create a new one."""
        if self._page is None or self._page.is_closed():
            context = await self.browser.new_context()
            self._page = await context.new_page()
        return self._page

    async def navigate(self, url):
        """Navigate to a URL and wait for the page to be ready."""
        page = await self.get_page()
        await page.goto(url, timeout=settings.BROWSER_TIMEOUT, wait_until="domcontentloaded")
        return page


manager = BrowserManager()