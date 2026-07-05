from app.utils.logger import logger 
from bs4 import BeautifulSoup 

class PageExtractor:

    async def extract_html(self,page):
        logger.info("Extracting HTML...")
        html = await page.content() 
        return html 
    
    async def parse_html(self,html):
        soup = await BeautifulSoup(html,"lxml")
        return soup
    
    async def extract_ax_tree(self,page):
        logger.info("Extracting Accessibility Tree...")
        ax_tree = await page.accessibility.snapshot()
        return ax_tree
    
    async def extract(self,page):
        html = await self.extract_html(page)
        soup = await self.parse_html(html)
        ax_tree = await self.extract_ax_tree(page)
        return {
            "html" : soup,
            "ax_tree" : ax_tree
        }