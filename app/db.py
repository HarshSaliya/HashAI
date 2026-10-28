from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import DB_CONN

pool = ConnectionPool(conninfo=DB_CONN, min_size=1, max_size=5, configure=register_vector, open=True)


class DB:
    def _connect(self):
        return pool.connection()

    def fetchone(self, query: str, params: tuple = None) -> dict:
        with self._connect() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def fetchall(self, query: str, params: tuple = None) -> list:
        with self._connect() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def insert(self, query: str, params) -> int:
        with self._connect() as conn:
            with conn.cursor() as cur:
                if isinstance(params, list):
                    cur.executemany(query, params)
                else:
                    cur.execute(query, params)
                return cur.rowcount

    def update(self, query: str, params: tuple = None) -> int:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    def delete(self, query: str, params: tuple = None) -> int:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    def run_transaction(self, statements: list) -> list:
        """statements: list of (query, params) run on one connection, one commit."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                counts = []
                for query, params in statements:
                    if isinstance(params, list):
                        cur.executemany(query, params)
                    else:
                        cur.execute(query, params)
                    counts.append(cur.rowcount)
                return counts
