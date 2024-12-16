import sys
import time

from dotenv import load_dotenv
from src.resy_notifier.api_client import ResyAPIClient
import os
from src.resy_notifier.db_manager import DatabaseManager
from src.resy_notifier.logger_config import setup_logger

load_dotenv()

# Initialize logger
logger = setup_logger()

def main(loop_limit=None):
    # Ensure correct number of arguments
    if len(sys.argv) < 2:
        # venue_url_name is mandatory
        print("Usage: python main.py <venue_url_name>")
        sys.exit(1)

    # Parse command-line arguments
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

    # Initialize state for availability tracking
    last_availability_state = None
    iterations = 0

    while True:
        try:
            logger.info(
                f"Sending request for venue_id={venue_id}, party_size={party_size}, start_date={start_date}, end_date={end_date}"
            )
            availability = client.get_availability(
                venue_id, venue_name, party_size, start_date, end_date
            )

            # Determine current availability state
            current_state = len(availability) > 0

            # Log state transitions
            if current_state and last_availability_state is None:
                logger.info(f"Availability detected for the first time at {venue_name}: {availability}")
            elif current_state and not last_availability_state:
                logger.info(f"Availability returned for {venue_name}: {availability}")
            elif not current_state and last_availability_state:
                logger.info(f"Availability disappeared for {venue_name}")
            elif not current_state:
                logger.info(f"No availability for {venue_name} (no change from last check).")

            # Update last state
            last_availability_state = current_state

            # Increment iteration counter and exit if limit is reached
            iterations += 1
            if loop_limit is not None and iterations >= loop_limit:
                break

            # Wait before next request
            time.sleep(request_interval)

        except Exception as e:
            logger.error(f"Error occurred: {e}", exc_info=True)
            sys.exit(1)
