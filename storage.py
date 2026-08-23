"""
Simple JSON-based storage replacing Redis.
No external dependencies - pure Python file storage.
Supports: get, set, delete, sadd, srem, smembers, sismember, setex
"""

import json
import os
import time
import threading
from typing import Any, Optional, Set, List

STORE_FILE = "data_store.json"
_lock = threading.Lock()


def _load_store() -> dict:
    """Load the JSON store from file."""
    if not os.path.exists(STORE_FILE):
        return {"strings": {}, "sets": {}, "expirations": {}}
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"strings": {}, "sets": {}, "expirations": {}}


def _save_store(store: dict):
    """Save the JSON store to file."""
    try:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False)
    except Exception as e:
        print(f"Storage save error: {e}")


def _cleanup_expired(store: dict):
    """Remove expired keys."""
    now = time.time()
    expired = [k for k, v in store.get("expirations", {}).items() if v < now]
    for k in expired:
        store.get("strings", {}).pop(k, None)
        store.get("sets", {}).pop(k, None)
        store.get("expirations", {}).pop(k, None)


class SimpleStorage:
    """Drop-in replacement for Redis using JSON file storage."""

    def __init__(self, host=None, port=None, db=None, password=None, **kwargs):
        # Accept Redis-style args but ignore them - we use file storage
        pass

    def get(self, key: str) -> Optional[str]:
        with _lock:
            store = _load_store()
            _cleanup_expired(store)
            return store.get("strings", {}).get(str(key))

    def set(self, key: str, value: Any) -> bool:
        with _lock:
            store = _load_store()
            store.setdefault("strings", {})[str(key)] = str(value) if not isinstance(value, str) else value
            _save_store(store)
        return True

    def setex(self, key: str, ttl: int, value: Any) -> bool:
        with _lock:
            store = _load_store()
            store.setdefault("strings", {})[str(key)] = str(value) if not isinstance(value, str) else value
            store.setdefault("expirations", {})[str(key)] = time.time() + int(ttl)
            _save_store(store)
        return True

    def delete(self, *keys: str) -> int:
        with _lock:
            store = _load_store()
            count = 0
            for key in keys:
                k = str(key)
                if k in store.get("strings", {}):
                    del store["strings"][k]
                    count += 1
                if k in store.get("sets", {}):
                    del store["sets"][k]
                    count += 1
                if k in store.get("expirations", {}):
                    del store["expirations"][k]
            _save_store(store)
        return count

    # Aliases
    def __delattr__(self, name):
        pass

    def sadd(self, key: str, *values: Any) -> int:
        with _lock:
            store = _load_store()
            k = str(key)
            s = store.setdefault("sets", {}).setdefault(k, [])
            count = 0
            for v in values:
                vstr = str(v) if not isinstance(v, str) else v
                if vstr not in s:
                    s.append(vstr)
                    count += 1
            _save_store(store)
        return count

    def srem(self, key: str, *values: Any) -> int:
        with _lock:
            store = _load_store()
            k = str(key)
            s = store.get("sets", {}).get(k, [])
            count = 0
            for v in values:
                vstr = str(v) if not isinstance(v, str) else v
                if vstr in s:
                    s.remove(vstr)
                    count += 1
            if count > 0:
                if not s:
                    store.get("sets", {}).pop(k, None)
                _save_store(store)
        return count

    def smembers(self, key: str) -> Set[str]:
        with _lock:
            store = _load_store()
            k = str(key)
            s = store.get("sets", {}).get(k, [])
            return set(s)

    def sismember(self, key: str, value: Any) -> bool:
        with _lock:
            store = _load_store()
            k = str(key)
            vstr = str(value) if not isinstance(value, str) else value
            return vstr in store.get("sets", {}).get(k, [])

    def exists(self, *keys: str) -> int:
        with _lock:
            store = _load_store()
            count = 0
            for key in keys:
                k = str(key)
                if k in store.get("strings", {}) or k in store.get("sets", {}):
                    count += 1
        return count

    def keys(self, pattern: str = "*") -> List[str]:
        import fnmatch
        with _lock:
            store = _load_store()
            all_keys = list(store.get("strings", {}).keys()) + list(store.get("sets", {}).keys())
            return [k for k in all_keys if fnmatch.fnmatch(k, pattern)]

    def ttl(self, key: str) -> int:
        with _lock:
            store = _load_store()
            k = str(key)
            if k in store.get("expirations", {}):
                remaining = int(store["expirations"][k] - time.time())
                return max(remaining, -2)
        return -1

    def expire(self, key: str, ttl: int) -> bool:
        with _lock:
            store = _load_store()
            k = str(key)
            if k in store.get("strings", {}) or k in store.get("sets", {}):
                store.setdefault("expirations", {})[k] = time.time() + int(ttl)
                _save_store(store)
                return True
        return False

    def incr(self, key: str, amount: int = 1) -> int:
        with _lock:
            store = _load_store()
            k = str(key)
            current = store.get("strings", {}).get(k, "0")
            try:
                val = int(current) + amount
            except (ValueError, TypeError):
                val = amount
            store.setdefault("strings", {})[k] = str(val)
            _save_store(store)
        return val

    def decr(self, key: str, amount: int = 1) -> int:
        return self.incr(key, -amount)
