import unittest
from unittest.mock import patch, Mock
from src.resy_notifier.email_helper import EmailHelper
from src.resy_notifier.model.availability import Availability, Inventory


class TestEmailHelper(unittest.TestCase):
    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    }, clear=True)
    def test_initialization_success(self, mock_load_dotenv):
        """
        Test that EmailHelper initializes correctly with valid environment variables.
        """
        email_helper = EmailHelper()
        self.assertEqual(email_helper.sender_email, "sender@example.com")
        self.assertEqual(email_helper.sender_password, "password")
        self.assertEqual(email_helper.recipient_email, "recipient@example.com")
        self.assertEqual(email_helper.smtp_server, "smtp.example.com")
        self.assertEqual(email_helper.smtp_port, "587")

    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    }, clear=True)
    def test_initialization_failure_missing_email_env_vars(self, mock_load_dotenv):
        """
        Test that EmailHelper raises a ValueError if required environment variables are missing.
        """
        with self.assertRaises(ValueError) as context:
            EmailHelper()
        self.assertIn("Email credentials are not set in environment variables.", str(context.exception))

    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_PORT": "587",
    }, clear=True)
    def test_initialization_failure_missing_smtp_env_vars(self, mock_load_dotenv):
        """
        Test that EmailHelper raises a ValueError if required environment variables are missing.
        """
        with self.assertRaises(ValueError) as context:
            EmailHelper()
        self.assertIn("SMTP Configuration is not set in environment variables.", str(context.exception))

    @patch("smtplib.SMTP")
    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    })
    def test_send_email_success(self, mock_load_dotenv, mock_smtp):
        """
        Test that send_email sends an email successfully.
        """
        email_helper = EmailHelper()

        # Mock the SMTP server
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call the method
        email_helper.send_email("Test Subject", "Test Body")

        # Assertions
        mock_smtp.assert_called_once_with("smtp.example.com", '587')
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("sender@example.com", "password")
        mock_server.send_message.assert_called_once()

    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    })
    def test_send_email_failure_missing_parameters(self, mock_load_dotenv):
        """
        Test that send_email raises a ValueError when subject or body is missing.
        """
        email_helper = EmailHelper()

        with self.assertRaises(ValueError) as context:
            email_helper.send_email("", "Test Body")
        self.assertIn("Subject and Body are required.", str(context.exception))

    @patch("smtplib.SMTP")
    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    })
    def test_check_and_notify_availability(self, mock_load_dotenv, mock_smtp):
        """
        Test check_and_notify_availability sends an email when there are available days.
        """
        email_helper = EmailHelper()

        # Mock the SMTP server
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Create test data
        availabilities = [
            Availability(date="2024-12-01", inventory=Inventory("available", "not available", "available")),
            Availability(date="2024-12-02", inventory=Inventory("sold-out", "not available", "not available")),
        ]

        # Call the method
        email_helper.check_and_notify_availability("Test Venue", availabilities)

        # Assertions
        mock_smtp.assert_called_once()
        mock_server.send_message.assert_called_once()

    @patch("smtplib.SMTP")
    @patch("src.resy_notifier.email_helper.load_dotenv")
    @patch.dict("os.environ", {
        "SENDER_EMAIL": "sender@example.com",
        "SENDER_PASSWORD": "password",
        "RECIPIENT_EMAIL": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
    })
    def test_check_and_notify_availability_no_available_days(self, mock_load_dotenv, mock_smtp):
        """
        Test check_and_notify_availability does not send an email when there are no available days.
        """
        email_helper = EmailHelper()

        # Create test data with no available days
        availabilities = [
            Availability(date="2024-12-01", inventory=Inventory("sold-out", "not available", "available")),
            Availability(date="2024-12-02", inventory=Inventory("closed", "not available", "not available")),
        ]

        # Call the method
        email_helper.check_and_notify_availability("Test Venue", availabilities)

        # Assertions
        mock_smtp.assert_not_called()


if __name__ == "__main__":
    unittest.main()
