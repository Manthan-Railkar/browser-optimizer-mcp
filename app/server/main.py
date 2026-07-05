from fastmcp import FastMcp
from app.config.settings import settings
from app.utils.logger import logger 
from app.browser.manager import manager
import asyncio

mcp = FastMcp("Browser Optimization MCP")

async def startup():
    await manager.start()

async def shutdown():
    await manager.stop()

logger.info("Initializing Browser Optimizer MCP...")
logger.info(f"Headless Mode: {settings.HEADLESS}")
logger.info(f"Log Level: {settings.LOG_LEVEL}")


if __name__ == "__main__":
    logger.info("Starting the MCP server...")
    asyncio.run(startup())
    try :
        mcp.run()
    finally:
        asyncio.run(shutdown())
