from fastapi import FastAPI
from app.config.database import get_db_connection
from app.controllers import product_controller
from app.controllers import order_controller
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter 
from app.controllers import product_controller

app = FastAPI(title="E-Commerce Mini API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include router
app.include_router(product_controller.router)

# Register Controllers / Routers
app.include_router(product_controller.router)
app.include_router(order_controller.router)

@app.get("/")
def root():
    return {"message": "API E-Commerce Berjalan!"}

@app.get("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), version();")
        db_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "status": "success",
            "message": "Koneksi ke PostgreSQL berhasil!",
            "details": db_info
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}