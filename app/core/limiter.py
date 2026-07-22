import os
import ssl
from slowapi import Limiter
from slowapi.util import get_remote_address

redis_url = os.getenv("REDIS_URL")

if redis_url:
    # 1. Pastikan memaksa protokol RESP2 (protocol=2) untuk Upstash
    if "protocol=" not in redis_url:
        delimiter = "&" if "?" in redis_url else "?"
        redis_url = f"{redis_url}{delimiter}protocol=2"

    # 2. Buka pengetatan SSL jika rediss:// (SSL) digunakan
    if "ssl_cert_reqs=" not in redis_url and redis_url.startswith("rediss://"):
        redis_url = f"{redis_url}&ssl_cert_reqs=none"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    strategy="fixed-window",
    storage_options={
        "socket_timeout": 5,
        "retry_on_timeout": True,
    }
)