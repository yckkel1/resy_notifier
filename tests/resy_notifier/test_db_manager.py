import pytest
from unittest.mock import patch, Mock
from db_manager import DatabaseManager
from mysql.connector import Error as MySQLError
from constants.queries import GET_ACTIVE_API_KEY

class TestDatabaseManager:
    @patch("mysql.connector.connect")
    def test_get_active_api_key_success(self, mock_connect):
        """Test retrieving an active API key successfully."""
        # Mock connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Mock the query result
        mock_cursor.fetchone.return_value = ("test_api_key",)

        # Instantiate the database manager
        db_manager = DatabaseManager()

        # Call the method
        api_key = db_manager.get_active_api_key()

        # Assertions
        assert api_key == "test_api_key"
        mock_connect.assert_called_once()  # Ensure the connection was made
        mock_cursor.execute.assert_called_once_with(GET_ACTIVE_API_KEY)
        mock_cursor.fetchone.assert_called_once()

    @patch("mysql.connector.connect")
    def test_get_active_api_key_not_found(self, mock_connect):
        """Test retrieving an API key when none are active."""
        # Mock connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Mock no results
        mock_cursor.fetchone.return_value = None

        # Instantiate the database manager
        db_manager = DatabaseManager()

        # Call the method and expect a ValueError
        with pytest.raises(ValueError, match="API key not found"):
            db_manager.get_active_api_key()

        # Assertions
        mock_connect.assert_called_once()  # Ensure the connection was made
        mock_cursor.execute.assert_called_once_with(GET_ACTIVE_API_KEY)
        mock_cursor.fetchone.assert_called_once()

    @patch("mysql.connector.connect")
    def test_get_active_api_key_db_error(self, mock_connect):
        """Test handling of database connection errors."""
        # Mock connection error
        mock_connect.side_effect = MySQLError("Database connection error")

        # Instantiate the database manager
        db_manager = DatabaseManager()

        # Call the method and expect a MySQLError
        with pytest.raises(MySQLError, match="Database connection error"):
            db_manager.get_active_api_key()

        # Ensure the connection was attempted
        mock_connect.assert_called_once()
