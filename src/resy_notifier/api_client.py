from dotenv import load_dotenv
import os
import httpx
from datetime import datetime, timedelta

class ResyAPIClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("RESY_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        if not self.api_key:
            raise ValueError("API key is missing. Set RESY_API_KEY in your .env file.")
        if not self.base_url:
            raise ValueError("Base URL is missing. Set BASE_URL in your .env file.")

    def get_availability(self, venue_id, start_date=None, end_date=None):
        """
        Fetch availability for a venue within a date range.

        Args:
            venue_id (int): The ID of the venue.
            start_date (str): Start date in 'YYYY-MM-DD' format. Defaults to today.
            end_date (str): End date in 'YYYY-MM-DD' format. Defaults to a week from today.

        Returns:
            dict: Parsed JSON response from the API.
        """
        # Compute default dates if not provided
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        # Define headers
        headers = {
            "Authorization": f'ResyAPI api_key="{self.api_key}"',
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }

        # Send request
        url = f"{self.base_url}/venue/calendar"
        params = {
            "venue_id": venue_id,
            "num_seats": 2,
            "start_date": start_date,
            "end_date": end_date,
        }
        response = httpx.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise error if response code isn't 2xx
        return response.json()
