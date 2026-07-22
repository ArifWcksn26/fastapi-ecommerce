import os
from slowapi import Limiter
from slowapi.util import get_remote_address

redis_url = os.getenv("REDIS_URL")

if redis_url:
    # 1. Pastikan protokol RESP2 (protocol=2) aktif untuk Upstash
    if "protocol=" not in redis_url:
        delimiter = "&" if "?" in redis_url else "?"
        redis_url = f"{redis_url}{delimiter}protocol=2"

    # 2. Tambahkan opsi bypass SSL langsung di URI jika menggunakan rediss://
    if redis_url.startswith("rediss://") and "ssl_cert_reqs=" not in redis_url:
        redis_url = f"{redis_url}&ssl_cert_reqs=none"

    # 3. Inisialisasi Limiter tanpa mengoper connection_pool/options yang konflik
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=redis_url,
        strategy="fixed-window"
    )
else:
    limiter = Limiter(key_func=get_remote_address)