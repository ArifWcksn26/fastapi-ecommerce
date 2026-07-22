import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Ambil REDIS_URL dari environment variable, jika tidak ada fallback ke localhost
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL
)