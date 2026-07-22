import os
import redis
from slowapi import Limiter
from slowapi.util import get_remote_address

redis_url = os.getenv("REDIS_URL")

# Inisialisasi Storage URI / Storage Instance
if redis_url:
    # Menggunakan redis.from_url dengan penanganan SSL & RESP2 yang aman untuk Upstash
    redis_client = redis.from_url(
        redis_url,
        protocol=2,               # Paksa RESP2 agar kompatibel dengan Upstash free tier
        ssl_cert_reqs=None,       # Bypass verifikasi sertifikat SSL di serverless
        socket_timeout=5,
        retry_on_timeout=True
    )
    
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=redis_url,
        strategy="fixed-window",
        storage_options={
            "connection_pool": redis_client.connection_pool
        }
    )
else:
    # Fallback ke in-memory limiter jika REDIS_URL tidak terdefinisi (misal lokal dev)
    limiter = Limiter(key_func=get_remote_address)