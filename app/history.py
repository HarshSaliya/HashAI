from app.config import HISTORY_LIMIT
from app.db import DB

RECENT_SQL = """SELECT question, answer
                 FROM chat_messages
                 WHERE session_id = %s
                 ORDER BY created_at DESC
                 LIMIT %s"""

SAVE_SQL = """INSERT INTO chat_messages (session_id, question, answer)
              VALUES (%s, %s, %s)"""


class ChatHistory:
    def __init__(self):
        self.db = DB()

    def get_recent(self, session_id, limit=HISTORY_LIMIT):
        rows = self.db.fetchall(RECENT_SQL, (session_id, limit))
        return list(reversed(rows))

    def save(self, session_id, question, answer):
        self.db.insert(SAVE_SQL, (session_id, question, answer))
