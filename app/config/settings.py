from dotenv import load_env
import os
load_env()

class Settings : 
    LOG_LEVEL=os.getenv("LOG_LEVEL","INFO")
    HEADLESS=os.getenv("HEADLESS","True") == "True"
    CACHE_ENABLED=os.getenv("CACHE_ENABLED","True")
    REDIS_URL=os.getenv("REDIS_URL","redis://localhost:6379")
    BROWSER_TIMEOUT= int(os.getenv("BROWSER_TIMEOUT","30000"))

settings = Settings() 