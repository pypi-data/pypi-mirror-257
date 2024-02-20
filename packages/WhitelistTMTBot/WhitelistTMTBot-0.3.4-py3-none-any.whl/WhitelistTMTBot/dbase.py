import logging
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            logger.info("Database connection established.")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def execute_query(self, query: str, params=()):
        try:
            with self.conn:
                self.conn.execute(query, params)
                logger.info("Query executed.")
        except sqlite3.Error as e:
            logger.error(f"Failed to execute query: {e}")
            raise

    def execute_read_query(self, query: str, params=()):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            logger.error(f"Failed to execute read query: {e}")
            raise

    def create_whitelist_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            uuid TEXT NOT NULL,
            bot TEXT NOT NULL
        );
        """
        self.execute_query(query)
        logger.info("Table 'whitelist' created.")

    def check_user_in_whitelist(self, user_id: str) -> bool:
        query = "SELECT 1 FROM whitelist WHERE user_id = ? LIMIT 1;"
        result = self.execute_read_query(query, (user_id,))
        return bool(result)

    def add_to_whitelist(self, user_id: str, uuid: str, bot: str):
        query = "INSERT INTO whitelist (user_id, uuid, bot) VALUES (?, ?, ?);"
        self.execute_query(query, (user_id, uuid, bot))
        logger.info(f"User {user_id} added to whitelist.")
