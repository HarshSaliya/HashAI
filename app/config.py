import os
from dotenv import load_dotenv


load_dotenv()


DB_CONN = os.getenv("DATABASE_URL")
GROQ_API = os.getenv("GROQ_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-m3")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# must match the model - bge-m3 is 1024, MiniLM is 384
TABLE_NAME = os.getenv("TABLE_NAME", "resume_chunks")
