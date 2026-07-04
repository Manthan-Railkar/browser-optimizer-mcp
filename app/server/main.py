from fastmcp import FastMcp
from app.config.settings import settings
from app.utils.logger import logger 

mcp = FastMcp("Browser Optimization MCP")

logger.info("Initializing Browser Optimizer MCP...")
logger.info(f"Headless Mode: {settings.HEADLESS}")
logger.info(f"Log Level: {settings.LOG_LEVEL}")

if __name__ == "__main__":
    logger.info("Starting the MCP server...")
    mcp.run()
