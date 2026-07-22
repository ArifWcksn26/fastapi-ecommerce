import json
from app.config.database import get_db_connection
from app.config.redis import get_redis_client

class ProductRepository:
    @staticmethod
    def get_all_products():
        redis_client = get_redis_client()
        cache_key = "products:all"

        # 1. Cek di Redis terlebih dahulu
        if redis_client:
            try:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    print("⚡ [CACHE HIT] Mengambil data produk dari Redis")
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Redis Error: {e}")

        # 2. Jika tidak ada di Redis (Cache Miss), ambil dari PostgreSQL
        print("🐢 [CACHE MISS] Mengambil data produk dari PostgreSQL")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                p.id, 
                p.name, 
                p.description, 
                p.price, 
                p.stock, 
                c.id as category_id,
                c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.id ASC;
        """
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        conn.close()

        # Konversi Decimal/Numeric ke float untuk JSON serialization
        for item in products:
            item['price'] = float(item['price'])

        # 3. Simpan hasil ke Redis dengan TTL (Time To Live) misal 300 detik (5 menit)
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(products))
            except Exception as e:
                print(f"Gagal simpan ke Redis: {e}")

        return 
    
    @staticmethod
    def invalidate_product_cache():
        """
        Menghapus cache ketika ada transaksi/stok berubah
        agar data yang di-cache tidak basi (stale data).
        """
        redis_client = get_redis_client()
        if redis_client:
            try:
                redis_client.delete("products:all")
                print("🧹 [CACHE INVALIDATED] Cache produk dibersihkan")
            except Exception as e:
                print(f"Gagal hapus cache: {e}")
    
    @staticmethod
    def create_order_transaction(user_id: int, items: list):
        """
        Membuat transaksi order dengan ACID Transaction (Commit/Rollback)
        items: list of dict, contoh: [{'product_id': 1, 'quantity': 2}]
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 1. Cek stok & hitung total harga
            total_amount = 0.0
            order_items_data = []

            for item in items:
                product_id = item['product_id']
                qty = item['quantity']

                # Lock row produk agar tidak terjadi race condition
                cursor.execute("SELECT price, stock FROM products WHERE id = %s FOR UPDATE;", (product_id,))
                product = cursor.fetchone()

                if not product:
                    raise Exception(f"Produk dengan ID {product_id} tidak ditemukan.")
                
                if product['stock'] < qty:
                    raise Exception(f"Stok produk ID {product_id} tidak mencukupi. Sisa stok: {product['stock']}")

                # Konversi Decimal ke float agar safe untuk JSON Serialization
                price_float = float(product['price'])
                item_total = price_float * qty
                total_amount += item_total

                order_items_data.append({
                    "product_id": product_id,
                    "quantity": qty,
                    "price": price_float
                })

            # 2. Insert ke tabel `orders`
            query_order = """
                INSERT INTO orders (user_id, total_amount, status)
                VALUES (%s, %s, 'completed')
                RETURNING id;
            """
            cursor.execute(query_order, (user_id, total_amount))
            order_id = cursor.fetchone()['id']

            # 3. Insert ke `order_items` & Update `stock` di `products`
            for item in order_items_data:
                # Insert order item
                query_item = """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query_item, (order_id, item['product_id'], item['quantity'], item['price']))

                # Deduct stock
                query_stock = """
                    UPDATE products 
                    SET stock = stock - %s 
                    WHERE id = %s;
                """
                cursor.execute(query_stock, (item['quantity'], item['product_id']))

            # Commit seluruh transaksi jika tidak ada error
            conn.commit()

            # Hapus cache produk karena stok barang baru saja di-update!
            ProductRepository.invalidate_product_cache()
            
            return {
                "order_id": order_id,
                "total_amount": float(total_amount),
                "items": order_items_data
            }

        except Exception as e:
            # Batalkan semua perubahan jika ada error/stok kurang
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_product_by_id(product_id: int):
        """
        Mengambil detail satu produk berdasarkan ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                p.id, 
                p.name, 
                p.description, 
                p.price, 
                p.stock, 
                c.id as category_id,
                c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = %s;
        """
        
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return product
    
    @staticmethod
    def get_order_detail(order_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query Header Order
        query_order = "SELECT id, user_id, total_amount, status, created_at FROM orders WHERE id = %s;"
        cursor.execute(query_order, (order_id,))
        order = cursor.fetchone()

        if not order:
            cursor.close()
            conn.close()
            return None

        # Query Items Order
        query_items = """
            SELECT oi.product_id, p.name as product_name, oi.quantity, oi.price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s;
        """
        cursor.execute(query_items, (order_id,))
        items = cursor.fetchall()

        cursor.close()
        conn.close()

        # Konversi Decimal ke float untuk JSON response
        order['total_amount'] = float(order['total_amount'])
        for item in items:
            item['price'] = float(item['price'])

        order['items'] = items
        return order