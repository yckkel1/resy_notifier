from dotenv import load_dotenv

from api_client import ResyAPIClient
from notifier import ResyNotifier

load_dotenv()

def main():
    client = ResyAPIClient()
    print(client.get_availability(834))

if __name__ == "__main__":
    main()
