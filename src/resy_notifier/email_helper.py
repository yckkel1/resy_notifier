import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
from model.availability import Availability


class EmailHelper:
    def __init__(self):
        """
        Initialize the EmailHelper by loading credentials from environment variables.
        Raises a ValueError if credentials are not set.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()

        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")

        if not self.sender_email or not self.sender_password:
            raise ValueError("Email credentials are not set in environment variables.")

        # SMTP server configuration (Gmail in this example)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, subject: str, body: str):
        """
        Send an email using the loaded credentials.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.

        Raises:
            ValueError: If any required parameter is missing.
            Exception: For errors during the email sending process.
        """
        if not subject or not body:
            raise ValueError("Subject and Body are required.")

        try:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade connection to secure
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"Email sent successfully")

        except Exception as e:
            raise Exception(f"Error sending email: {e}")

    def check_and_notify_availability(self, venue_name: str, availability: list[Availability]):
        """
        Check availability in the calendar and send email notifications if available.

        Args:
            venue_name (str): The name of the venue.
            availability (list<Availability>): The parsed availability data returned by the API.
        """
        available_days = []
        for day in availability:
            if day.inventory.reservation == "available":  # Use dot notation for object attributes
                available_days.append(
                    f"Date: {day.date}\n"
                    f"- Reservation: {day.inventory.reservation}\n"
                    f"- Event: {day.inventory.event}\n"
                    f"- Walk-in: {day.inventory.walk_in}\n"
                )

        # If no days are available, do nothing
        if not available_days:
            return

        # Prepare the email content
        subject = f"Reservation Availability for {venue_name}"
        body = (
                f"Good news! There are available reservations for {venue_name}.\n\n"
                f"Details:\n\n" + "\n\n".join(available_days)
        )
        self.send_email(subject, body)