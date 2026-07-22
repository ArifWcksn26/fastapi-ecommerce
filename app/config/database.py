import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

def get_db_connection():
    """
    Fungsi untuk membuat koneksi ke database PostgreSQL.
    Menggunakan RealDictCursor agar hasil query dikembalikan dalam bentuk Dictionary/JSON-like.
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as error:
        print(f"Error koneksi ke database: {error}")
        raise error