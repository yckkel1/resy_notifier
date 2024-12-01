from dotenv import load_dotenv
from api_client import ResyAPIClient
import os

load_dotenv()

def main():
    api_key = os.getenv("RESY_API_KEY")
    base_url = os.getenv("BASE_URL")
    client = ResyAPIClient(api_key, base_url)
    print(client.get_availability(834))

if __name__ == "__main__":
    main()
