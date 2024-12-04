import os
from dotenv import load_dotenv
import mysql.connector
from constants.queries import GET_ACTIVE_API_KEY

class DatabaseManager:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Database configuration loaded from environment variables
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_active_api_key(self):
        """
        Retrieve the most recent active API key.

        Returns:
            str: The API key, or raise error
        """

        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(GET_ACTIVE_API_KEY)
                result = cursor.fetchone()
                if not result:
                    raise ValueError("API key not found")
                return result[0]
        except mysql.connector.Error as e:
            print(f"Database error occurred: {e}")
            raise
