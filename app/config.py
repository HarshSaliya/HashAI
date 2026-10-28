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

RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")

# prior Q&A pairs resent per /ask call, oldest dropped first
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "10"))

# comma-separated IPs of reverse proxies we trust to set X-Forwarded-For. connecting IP, which is correct for an unproxied deployment.
TRUSTED_PROXIES = {
    ip.strip() for ip in os.getenv("TRUSTED_PROXIES", "").split(",") if ip.strip()
}
