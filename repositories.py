import os
import sqlite3
import logging
from models import ProductOut

# Путь к БД теперь для продуктов
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "products.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                in_stock BOOLEAN NOT NULL DEFAULT 1
            )
        """)
    conn.close()
    logger.info("Database initialized")

class ProductRepository:
    """Репозиторий для работы с таблицей products."""

    def create(self, name: str, price: int, in_stock: bool) -> ProductOut:
        """Создаёт новый продукт и возвращает его."""
        logger.info(f"Creating product: {name}, price={price}, in_stock={in_stock}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, in_stock) VALUES (?, ?, ?)",
                (name, price, in_stock)
            )
            product_id = cur.lastrowid
            conn.commit()

            cur.execute(
                "SELECT id, name, price, in_stock FROM products WHERE id = ?",
                (product_id,)
            )
            row = cur.fetchone()
            return ProductOut(**row)
        finally:
            conn.close()

    def get_all(self, min_price: int = None, max_price: int = None, in_stock: bool = None) -> list[ProductOut]:
        logger.info(f"Fetching products with filters: min_price={min_price}, max_price={max_price}, in_stock={in_stock}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            query = "SELECT id, name, price, in_stock FROM products WHERE 1=1"
            params = []
            if min_price is not None:
                query += " AND price >= ?"
                params.append(min_price)
            if max_price is not None:
                query += " AND price <= ?"
                params.append(max_price)
            if in_stock is not None:
                query += " AND in_stock = ?"
                params.append(1 if in_stock else 0)

            cur.execute(query, params)
            rows = cur.fetchall()
            return [ProductOut(**row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, product_id: int) -> ProductOut | None:
        logger.info(f"Fetching product by id: {product_id}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, price, in_stock FROM products WHERE id = ?",
                (product_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return ProductOut(**row)
        finally:
            conn.close()

    def update(self, product_id: int, name: str, price: int, in_stock: bool) -> ProductOut | None:
        logger.info(f"Updating product id={product_id}: name={name}, price={price}, in_stock={in_stock}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET name = ?, price = ?, in_stock = ? WHERE id = ?",
                (name, price, in_stock, product_id)
            )
            conn.commit()
            if cur.rowcount == 0:
                return None

            cur.execute(
                "SELECT id, name, price, in_stock FROM products WHERE id = ?",
                (product_id,)
            )
            row = cur.fetchone()
            return ProductOut(**row)
        finally:
            conn.close()

    def delete(self, product_id: int) -> bool:
        logger.info(f"Deleting product id={product_id}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()
