import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

from app.config import DB_CONN


class DB:
    def __init__(self):
        self.conn_str = DB_CONN

    def _connect(self):
        conn = psycopg.connect(self.conn_str)
        register_vector(conn)
        return conn

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
