import os
from slowapi import Limiter
from slowapi.util import get_remote_address

redis_url = os.getenv("REDIS_URL")

# Tambahkan query parameter protocol=2 jika menggunakan URL string
if redis_url and "protocol=" not in redis_url:
    delimiter = "&" if "?" in redis_url else "?"
    redis_url = f"{redis_url}{delimiter}protocol=2"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    strategy="fixed-window",
    storage_options={
        "socket_timeout": 5,
        "retry_on_timeout": True,
        "ssl_cert_reqs": None,  # Mencegah isu SSL handshake
    }
)