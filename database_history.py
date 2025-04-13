import sqlite3
from datetime import datetime
from typing import List, Optional

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from pydantic import BaseModel, Field

class DatabaseHistory():
    """Database implementation of chat message history."""

    def __init__(self, session_id: str, db_path: str = "chat_history.db"):
        self.session_id = session_id
        self.db_path = db_path
        
        # init db connection
        self._init_db()

    # create connection with database
    def _init_db(self):
        """Initialize the database and create the table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message TEXT NOT NULL,
                message_type TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def add_messages(self, session_id: str, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for message in messages:
            message_type = "human" if isinstance(message, HumanMessage) else "ai"
            cursor.execute(
                """
                INSERT INTO chat_history (session_id, message, message_type, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session_id,
                    message.content,
                    message_type,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        conn.commit()
        conn.close()

    def clear(self) -> None:
        """Clear all messages for the session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (self.session_id,))
        conn.commit()
        conn.close()

    def get_messages(self) -> List[BaseMessage]:
        """Retrieve all messages for the session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT message, message_type FROM chat_history WHERE session_id = ? ORDER BY timestamp",
            (self.session_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        messages = []
        for row in rows:
            message, message_type = row
            if message_type == "human":
                messages.append(HumanMessage(content=message))
            else:
                messages.append(AIMessage(content=message))
        return messages
    
if __name__ == "__main__":

    dbhistory = DatabaseHistory(session_id="1")
    