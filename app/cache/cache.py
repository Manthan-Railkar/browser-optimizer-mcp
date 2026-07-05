import time
import xxhash
from cachetools import TTLCache
from typing import Dict, Any, Optional
from app.config.settings import settings
from app.utils.logger import logger

class SemanticCache:
    def __init__(self, enabled: Optional[bool] = None, ttl: Optional[int] = None, max_size: Optional[int] = None):
        # Local TTL Cache using settings.
        # Max size is number of pages, TTL is in seconds.
        self.enabled = settings.CACHE_ENABLED if enabled is None else enabled
        self.ttl = settings.CACHE_TTL if ttl is None else ttl
        self.max_size = settings.CACHE_MAX_SIZE if max_size is None else max_size
        
        self._cache = TTLCache(maxsize=self.max_size, ttl=self.ttl)
        # Maps URL to the last page hash to check for changes
        self._url_to_hash: Dict[str, str] = {}
        logger.info(f"Semantic Cache initialized: Enabled={self.enabled}, TTL={self.ttl}s, MaxSize={self.max_size}")

    def generate_hash(self, text: str) -> str:
        """Generate a fast hash of the text content."""
        return xxhash.xxh64(text.encode('utf-8', errors='ignore')).hexdigest()

    def lookup(self, url: str, current_html: str) -> Optional[Dict[str, Any]]:
        """
        Check if we have a valid cache entry for the page HTML and URL.
        """
        if not self.enabled:
            return None
            
        current_hash = self.generate_hash(current_html)
        cached_entry = self._cache.get(url)
        
        if cached_entry:
            cached_hash = cached_entry.get("hash")
            if cached_hash == current_hash:
                logger.info(f"Cache HIT for URL: {url}")
                return cached_entry.get("context")
            else:
                logger.info(f"Cache MISMATCH (HTML changed) for URL: {url}")
        else:
            logger.info(f"Cache MISS for URL: {url}")
            
        # Store the current hash to associate with the URL
        self._url_to_hash[url] = current_hash
        return None

    def store(self, url: str, html: str, compressed_context: Dict[str, Any]):
        """
        Cache the compressed context for a URL associated with its current HTML hash.
        """
        if not self.enabled:
            return
            
        page_hash = self.generate_hash(html)
        self._cache[url] = {
            "hash": page_hash,
            "context": compressed_context,
            "timestamp": time.time()
        }
        self._url_to_hash[url] = page_hash
        logger.info(f"Cached context for URL: {url} (Hash: {page_hash})")

    def clear(self):
        self._cache.clear()
        self._url_to_hash.clear()
        logger.info("Cache cleared")

semantic_cache = SemanticCache()
