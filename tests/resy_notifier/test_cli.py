import unittest
from unittest.mock import patch, Mock, call
from src.resy_notifier.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.patcher_sys_argv = patch("sys.argv", [
            "main.py",
            "una-pizza-napoletana",
            "4",
            "2024-12-01",
            "2024-12-07",
            "2"
        ])
        self.mock_sys_argv = self.patcher_sys_argv.start()

        self.patcher_sleep = patch("time.sleep", return_value=None)
        self.mock_sleep = self.patcher_sleep.start()

        self.patcher_logger = patch("src.resy_notifier.cli.logger")
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_sys_argv.stop()
        self.patcher_sleep.stop()
        self.patcher_logger.stop()

    @patch("src.resy_notifier.cli.ResyAPIClient")
    @patch("src.resy_notifier.cli.DatabaseManager")
    def test_main(self, mock_db_manager, mock_api_client):
        mock_db_instance = Mock()
        mock_db_instance.get_active_api_key.return_value = "test_api_key"
        mock_db_instance.get_venue_info.return_value = (12345, "Una Pizza Napoletana")
        mock_db_manager.return_value = mock_db_instance

        mock_client_instance = Mock()
        mock_client_instance.get_availability.side_effect = [
            [], [], [{"date": "2024-12-01", "inventory": {"reservation": "available"}}]
        ]
        mock_api_client.return_value = mock_client_instance

        main(loop_limit=3)  # Limit the loop to 3 iterations

        mock_db_instance.get_active_api_key.assert_called_once()
        mock_db_instance.get_venue_info.assert_called_once_with("una-pizza-napoletana")
        mock_api_client.assert_called_once_with("test_api_key", "https://api.resy.com/4")
        self.assertEqual(mock_client_instance.get_availability.call_count, 3)

        self.mock_logger.info.assert_has_calls([
            call('Sending request for venue_id=12345, party_size=4, start_date=2024-12-01, end_date=2024-12-07'),
            call("No availability for Una Pizza Napoletana (no change from last check)."),
            call("Sending request for venue_id=12345, party_size=4, start_date=2024-12-01, end_date=2024-12-07"),
            call("No availability for Una Pizza Napoletana (no change from last check)."),
            call('Sending request for venue_id=12345, party_size=4, start_date=2024-12-01, end_date=2024-12-07'),
            call("Availability returned for Una Pizza Napoletana: [{'date': '2024-12-01', 'inventory': {'reservation': 'available'}}]")
        ])
