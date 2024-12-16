from datetime import datetime, timedelta
import httpx
from src.resy_notifier.model.availability import parse_response
from src.resy_notifier.email_helper import EmailHelper

class ResyAPIClient:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.email_helper = EmailHelper()
        if not self.api_key:
            raise ValueError("API key is required.")
        if not self.base_url:
            raise ValueError("Base URL is required.")

    def get_availability(self, venue_id, venue_name="", party_size=2, start_date=None, end_date=None):
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
            "num_seats": party_size,
            "start_date": start_date,
            "end_date": end_date,
        }

        try:
            response = httpx.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Parse the response
            availability = parse_response(response.json())
            print(availability)
            self.email_helper.check_and_notify_availability(venue_name, availability)
            return availability

        except httpx.RequestError as e:
            raise ValueError(f"Network error occurred: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Venue ID {venue_id} not found.")
            raise ValueError(f"HTTP error occurred: {e}")
        except ValueError as e:
            raise ValueError(f"Error parsing response: {e}")
