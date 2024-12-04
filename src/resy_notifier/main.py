from dotenv import load_dotenv
from api_client import ResyAPIClient
import os
from db_manager import DatabaseManager

load_dotenv()

def main():
    db_manager = DatabaseManager()
    api_key = db_manager.get_active_api_key()
    base_url = os.getenv("BASE_URL")
    client = ResyAPIClient(api_key, base_url)
    print(client.get_availability(834))

if __name__ == "__main__":
    main()
