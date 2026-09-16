import time
from threading import RLock


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int = 60):
        self.limit = max(1, limit)
        self.window = max(1, window_seconds)
        self._hits = {}
        self._lock = RLock()

    def allow(self, key: str) -> tuple[bool, int]:
        now = time.time()
        with self._lock:
            hits = [t for t in self._hits.get(key, []) if now - t < self.window]
            if len(hits) >= self.limit:
                retry_after = max(1, int(self.window - (now - hits[0])))
                self._hits[key] = hits
                return False, retry_after
            hits.append(now)
            self._hits[key] = hits
            return True, 0

    def clear(self):
        with self._lock:
            self._hits.clear()
