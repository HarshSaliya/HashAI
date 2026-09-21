import os
from dotenv import load_dotenv
import psycopg


load_dotenv()

db_conn = os.getenv("DATABASE_URL")

print(db_conn)

p=psycopg.connect(db_conn)

with psycopg.connect(db_conn)as conn:
    with conn.cursor() as cur:
        cur.execute("select version()")
        print(cur.fetchone())

print("Check DB" ,p)

