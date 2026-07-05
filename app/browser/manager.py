from playwright.async_api import async_playwright
from app.config.settings import settings
from app.utils.logger import logger 

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    async def start(self):
        logger.info("Starting Browser...")
        self.playwright = await async_playwright.start()
        self.browser = await self.playwright.chromium.launch(
            headless = settings.HEADLESS
        )
        logger.info("Chromium Started")

    async def stop(self):
        logger.info("Stopping Browser...")
        
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop() 
        
        logger.info("Chromium Stopped")
    
    async def new_context(self):
        return self.browser.new_context() 
    
    async def new_page(self):
        context = await self.new_context()
        page = await context.new_page()
        return page 
    

manager = BrowserManager()