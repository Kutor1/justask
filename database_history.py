from typing import List
import sqlite3
import json
from datetime import datetime
from langchain.schema import BaseChatMessageHistory, messages_from_dict
from langchain.schema.messages import BaseMessage

class DataBaseHistory(BaseChatMessageHistory):
    """store history in database"""
    
    # db_path = "chat_histories.db"

    def __init__(self, session_id:str, db_path: str = "chat_histories.db"):
        self.session_id = session_id
        self.db_path = db_path
        self._setup_database()

    def _setup_database(self):
        """init the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS message_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS session_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(session_id)
                )
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_session 
                ON message_history (session_id)
            ''')
            conn.commit()

    def add_session(self):
        '''
        add session_id into the database
        if it exists, then jump
        '''
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR IGNORE INTO session_history (session_id)
                VALUES (?)
            ''', self.session_id)

    def delete_session(self):
        '''delete session_id in dbase'''
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM session_history WHERE session_id = ?
            ''', self.session_id)

    @staticmethod
    def get_session():

        db_path = "chat_histories.db"

        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT session_id, created_at FROM session_history"
            )
        
        return cursor.fetchall()

    def get_messages_by_session(self):
        """
        use session_id select messages from database
        :param session_id
        :return: messages dict
        """
        messages = []
        
        try:

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT message 
                FROM message_history 
                WHERE session_id = ?
            """
            
            cursor.execute(query, (self.session_id,))
            results = cursor.fetchall()

            # parse from JSON
            for row in results:
                try:
                    message = json.loads(row[0])
                    messages.append({
                        "type": message["type"],
                        "data": message["data"]
                    })
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"parse the message from data failed: {str(e)}")

        except sqlite3.Error as e:
            print(f"connected database failed: {str(e)}")
        finally:
            if conn:
                conn.commit()

        return messages

    def add_message(self, message: BaseMessage) -> None:
        """build standard message before storing the message"""
        # build standard dict which messages_from_dict required
        message_data = {
            "type": message.type,  # use type factor（LangChain 0.1.0+）
            "data": {
                "content": message.content,
                # keep additional kwargs
                **message.additional_kwargs
            }
        }
        serialized = json.dumps(message_data)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO message_history (session_id, message) VALUES (?, ?)",
                (self.session_id, serialized)
            )
            conn.commit()

    def clear(self) -> None:
        """clear the message history for specific session_id"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM message_history WHERE session_id = ?",
                (self.session_id,)
            )
            conn.commit()

    @property
    def messages(self) -> List[BaseMessage]:
        """extract message history from the dbase"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT message FROM message_history "
                "WHERE session_id = ? "
                "ORDER BY created_at ASC",
                (self.session_id,)
            )
            items = [json.loads(row[0]) for row in cursor.fetchall()]
            
        return messages_from_dict(items)

if __name__ == "__main__":

    print(DataBaseHistory(session_id="1").get_messages_by_session())
    # print(DataBaseHistory.get_session())
    # db = DataBaseHistory(session_id="2")
    # db.add_session()