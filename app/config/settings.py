from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    HEADLESS = os.getenv("HEADLESS", "True") == "True"
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True") == "True"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
    CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "100"))
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))


settings = Settings()