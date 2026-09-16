from collections import Counter
from threading import RLock


class Metrics:
    def __init__(self):
        self._lock = RLock()
        self.requests = Counter()
        self.errors = Counter()

    def record_request(self, path: str, status: int):
        with self._lock:
            self.requests[f"{path}:{status}"] += 1

    def record_error(self, code: str):
        with self._lock:
            self.errors[code] += 1

    def snapshot(self) -> dict:
        with self._lock:
            return {"requests": dict(self.requests), "errors": dict(self.errors)}


metrics = Metrics()
