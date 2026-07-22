import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        # Cek apakah ada DATABASE_URL utuh (misal dari Vercel/Supabase)
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            connection = psycopg2.connect(
                db_url,
                cursor_factory=RealDictCursor
            )
        else:
            # Fallback ke konfigurasi per-variable (lokal)
            connection = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", ""),
                dbname=os.getenv("DB_NAME", "postgres"),
                cursor_factory=RealDictCursor
            )
        return connection
    except Exception as error:
        print(f"Error koneksi ke database: {error}")
        raise error