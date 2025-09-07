import sqlite3
import json
import logging
import threading
from datetime import datetime
from typing import List, Dict, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use a thread-local variable to manage connections, making it safe for multi-threaded use.
local = threading.local()

def get_db_connection():
    """Gets a thread-safe database connection."""
    if not hasattr(local, "connection"):
        local.connection = sqlite3.connect("jarvis_memory.db", check_same_thread=False)
        local.connection.row_factory = sqlite3.Row
    return local.connection

def initialize_database():
    """Initializes the database and creates the conversations table if it doesn't exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT,
                timestamp REAL NOT NULL,
                messages TEXT NOT NULL,
                metadata TEXT
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")

# Initialize the database once when the module is loaded.
initialize_database()

class ConversationMemory:
    """Handles persistent conversation memory for users using an SQLite database."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.conn = get_db_connection()
        logger.info(f"ConversationMemory initialized for user: {self.user_id}")

    def save_conversation(self, conversation: Union[Dict, object]) -> bool:
        """Saves a conversation to the database."""
        logger.info(f"Attempting to save conversation for user {self.user_id}")
        
        try:
            # Convert Pydantic object to dict if necessary
            if hasattr(conversation, 'model_dump'):
                convo_dict = conversation.model_dump()
            else:
                convo_dict = dict(conversation)

            messages_json = json.dumps(convo_dict.get("messages", []))
            timestamp = convo_dict.get("timestamp", datetime.now().timestamp())
            
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (user_id, timestamp, messages) VALUES (?, ?, ?)",
                (self.user_id, timestamp, messages_json)
            )
            self.conn.commit()
            
            logger.info(f"Successfully saved conversation for user {self.user_id} at timestamp {timestamp}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Failed to save conversation due to database error: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during save: {e}")
            return False

    def get_recent_context(self, max_messages: int = 30) -> List[Dict]:
        """
        Gets recent conversation context for the agent by fetching the latest messages
        from the database.
        """
        try:
            cursor = self.conn.cursor()
            # Fetch the most recent conversation entries for the user
            cursor.execute(
                "SELECT messages FROM conversations WHERE user_id = ? ORDER BY timestamp DESC",
                (self.user_id,)
            )
            
            all_messages = []
            rows = cursor.fetchall()
            
            # Iterate through rows and accumulate messages until the limit is reached
            for row in rows:
                messages_from_db = json.loads(row['messages'])
                all_messages.extend(messages_from_db)
                if len(all_messages) >= max_messages:
                    break
            
            # We get messages in reverse chronological order, so we need to reverse them back
            recent_messages = all_messages[:max_messages]
            recent_messages.reverse()

            logger.info(f"Retrieved {len(recent_messages)} recent messages for user {self.user_id}")
            return recent_messages

        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve recent context due to database error: {e}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching context: {e}")
            return []

    def get_conversation_count(self) -> int:
        """Gets the total number of saved conversation entries for this user."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM conversations WHERE user_id = ?",
                (self.user_id,)
            )
            count = cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            logger.error(f"Failed to get conversation count: {e}")
            return 0
