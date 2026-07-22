import os
import redis
from dotenv import load_dotenv

load_dotenv()

def get_redis_client():
    """
    Membuat koneksi ke Redis Server
    """
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True # Agar output otomatis berupa string, bukan bytes
        )
        return client
    except Exception as e:
        print(f"Error koneksi Redis: {e}")
        return None