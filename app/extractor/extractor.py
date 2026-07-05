from app.utils.logger import logger
from bs4 import BeautifulSoup


class PageExtractor:

    async def extract_html(self, page):
        logger.info("Extracting HTML...")
        html = await page.content()
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        return soup

    async def extract_ax_tree(self, page):
        logger.info("Extracting Accessibility Tree...")
        try:
            ax_tree = await page.locator("body").aria_snapshot()
            return ax_tree
        except Exception as e:
            logger.warning(f"Failed to extract ARIA snapshot: {e}")
            return None

    async def extract(self, page):
        html = await self.extract_html(page)
        soup = self.parse_html(html)
        ax_tree = await self.extract_ax_tree(page)

        return {
            "html": soup,
            "ax_tree": ax_tree,
            "raw_html_length": len(html),
            "url": page.url,
            "title": await page.title()
        }


extractor = PageExtractor()