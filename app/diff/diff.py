from typing import List, Dict, Any, Optional
from app.utils.logger import logger

class StateDifferenceEngine:
    def __init__(self):
        # Maps URL to the list of elements from the last observation
        self.history: Dict[str, List[Dict[str, Any]]] = {}

    def compute_diff(self, url: str, current_ui: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare the current list of UI elements with the last observed list for a URL.
        Returns a dictionary with 'added', 'removed', and 'changed' elements.
        """
        previous_ui = self.history.get(url, [])
        
        # Simple fingerprint for identifying matching elements
        def get_fingerprint(el: Dict[str, Any]) -> str:
            # Join key fields to uniquely identify the element
            tag = el.get("tag") or ""
            el_id = el.get("id") or ""
            name = el.get("name") or ""
            text = el.get("text") or ""
            placeholder = el.get("placeholder") or ""
            return f"{tag}|{el_id}|{name}|{text[:30]}|{placeholder}"

        prev_fingerprints = {get_fingerprint(el): el for el in previous_ui}
        curr_fingerprints = {get_fingerprint(el): el for el in current_ui}

        added = []
        removed = []
        changed = []

        # Find added elements
        for fp, el in curr_fingerprints.items():
            if fp not in prev_fingerprints:
                added.append(el)

        # Find removed elements
        for fp, el in prev_fingerprints.items():
            if fp not in curr_fingerprints:
                removed.append(el)

        # Store current state in history
        self.history[url] = current_ui
        logger.info(f"Diff computed for {url}: {len(added)} added, {len(removed)} removed")

        return {
            "url": url,
            "added": added,
            "removed": removed,
            "changed": changed  # Reserved for future deep attribute comparison
        }

    def clear_history(self, url: Optional[str] = None):
        if url:
            self.history.pop(url, None)
        else:
            self.history.clear()

difference_engine = StateDifferenceEngine()
