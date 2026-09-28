import os
from dotenv import load_dotenv


load_dotenv()


DB_CONN = os.getenv("DATABASE_URL")
GROQ_API = os.getenv("GROQ_API_KEY")
