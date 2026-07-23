# 🛒 FastAPI E-Commerce API (Serverless Architecture)

A high-performance RESTful API for an e-commerce backend built with **FastAPI**, **PostgreSQL (Supabase)**, and **Upstash Redis**, designed for serverless deployment on **Vercel**.

---

## 📸 Overview Architecture & Features

* **High Performance Caching**: Redis caching (Upstash via TLS) for frequent product catalog queries (`products:all`) with auto-invalidation on stock updates.
* **ACID Transactions & Concurrency Handling**: Row-level locking (`FOR UPDATE`) on PostgreSQL during order creation to prevent **race conditions** and stock overselling.
* **Rate Limiting**: Integrated Slowapi rate limiter on key endpoints to protect against DDoS and abuse.
* **Serverless Optimized**: Configured connection pooling and storage options tailored for Vercel's serverless runtime.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python 3.10+)
* **Database:** PostgreSQL (Supabase)
* **Cache Provider:** Upstash Redis (Serverless TLS)
* **Deployment:** Vercel
* **Security & Utility:** Slowapi (Rate Limiter), `psycopg2` / `SQLAlchemy`

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Supabase Account & Database
* Upstash Redis Account

### 2. Environment Variables
Create a `.env` file in the root directory:

`env
# Gunakan Port 6543 (Transaction Pooler) untuk Serverless/Vercel
DATABASE_URL=postgresql://<user>:<password>@<supabase-host>:6543/<dbname>
REDIS_URL=rediss://default:<password>@<upstash-host>:6379
```
```
# Clone repository
git clone [https://github.com/username/your-repo-name.git](https://github.com/username/your-repo-name.git)
cd your-repo-name

# Setup Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Server
uvicorn app.main:app --reload

## 👤 Author

* **Arif Wicaksono** - [GitHub Profile](https://github.com/ArifWcksn26)
