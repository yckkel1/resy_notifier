import sys
import time

from dotenv import load_dotenv
from api_client import ResyAPIClient
import os
from db_manager import DatabaseManager

load_dotenv()

def main():
    # Ensure correct number of arguments
    if len(sys.argv) < 2:
        # venue_url_name is mandatory
        print("Usage: python main.py <venue_url_name>")
        sys.exit(1)

    # Parse command-line arguments
    while True:
        try:
            venue_url_name = sys.argv[1]
            party_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2  # Default to 2
            start_date = sys.argv[3] if len(sys.argv) > 3 else None    # Default to today
            end_date = sys.argv[4] if len(sys.argv) > 4 else None      # Default to today + 14
            request_interval = sys.argv[5] if len(sys.argv) > 5 else 60 # Default to 1 Request/min
        except ValueError:
            print("Invalid party size. It must be an integer.")
            sys.exit(1)
        db_manager = DatabaseManager()
        api_key = db_manager.get_active_api_key()
        venue_id, venue_name = db_manager.get_venue_info(venue_url_name)
        base_url = os.getenv("BASE_URL")
        client = ResyAPIClient(api_key, base_url)
        availability = client.get_availability(venue_id, venue_name, party_size, start_date, end_date)
        if len(availability) > 0:
            # Avoid Spamming emails; Exit upon finding availability
            break
        time.sleep(request_interval)

if __name__ == "__main__":
    main()
