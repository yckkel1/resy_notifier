import os
from dotenv import load_dotenv
import mysql.connector
from constants.queries import GET_ACTIVE_API_KEY, GET_VENUE_INFO

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

    def get_active_api_key(self) -> str:
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

    def get_venue_info(self, url_name: str) -> tuple:
        """
        Retrieve the venue info for a given venue.

        Args:
            url_name (str): The venue name in url format. example: una-pizza-napoletana

        Returns:
            tuple: (venue_id: int, venue_name: str)

        Raises:
            ValueError: If no venue is found with the given name.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(GET_VENUE_INFO, (url_name,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"Venue '{url_name}' not found in the database.")
                return result
        except mysql.connector.Error as e:
            raise e
