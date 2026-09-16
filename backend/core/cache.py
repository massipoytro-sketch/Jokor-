import time
from threading import RLock


class TTLCache:
    def __init__(self):
        self._items = {}
        self._lock = RLock()

    def get(self, key):
        with self._lock:
            item = self._items.get(key)
            if not item:
                return None
            value, expires = item
            if expires <= time.time():
                self._items.pop(key, None)
                return None
            return value

    def set(self, key, value, ttl):
        with self._lock:
            self._items[key] = (value, time.time() + ttl)

    def delete(self, key):
        with self._lock:
            self._items.pop(key, None)

    def clear(self):
        with self._lock:
            self._items.clear()

    def size(self):
        with self._lock:
            return len(self._items)
