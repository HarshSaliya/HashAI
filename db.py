import os

import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

load_dotenv()


class DB:
    def __init__(self):
        self.conn_str = os.getenv("DATABASE_URL")

    def _connect(self):
        conn = psycopg.connect(self.conn_str)
        register_vector(conn)
        return conn

    def fetchone(self, query: str, params: tuple = None) -> dict:
        """Get a single row as a dict, or None if nothing matched."""
        with self._connect() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def fetchall(self, query: str, params: tuple = None) -> list:
        """Get all matching rows as a list of dicts."""
        with self._connect() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def insert(self, query: str, params) -> int:
        """Insert one row (tuple) or many (list of tuples). Returns rowcount."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                if isinstance(params, list):
                    cur.executemany(query, params)
                else:
                    cur.execute(query, params)
                return cur.rowcount

    def update(self, query: str, params: tuple = None) -> int:
        """Update rows. Returns number of rows changed."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    def delete(self, query: str, params: tuple = None) -> int:
        """Delete rows. Returns number of rows removed."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount
