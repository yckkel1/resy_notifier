
# ResyNotifier

ResyNotifier is a Python-based application designed to check restaurant availability on Resy.
It queries availability dynamically based on venue, party size, and date range, and sends email notifications when reservations become available.

---

## Features
- **Dynamic Availability Search**: Specify venue, party size, and date range dynamically via the command line.
- **Email Notifications**: Sends a notification when availability is detected.
- **Database Integration**: Retrieves active API keys and venue details from a MySQL database.
- **Configurable Interval**: Specify the interval for checking availability to avoid unnecessary API calls.
- **Graceful Termination**: Stops the script upon finding availability.

---

## Prerequisites
1. **Python 3.10+**
2. **MySQL Server** for storing API keys and venue information.
   3. **Environment Configuration**:
      - Use a `.env` file to manage sensitive credentials:
        ```plaintext
        BASE_URL=https://api.resy.com/4
        DB_HOST=
        DB_PORT=
        DB_USER=
        DB_PASSWORD=
        SENDER_EMAIL=
        SENDER_PASSWORD=
        RECIPIENT_EMAIL=
        SMTP_SERVER=
        SMTP_PORT=
        ```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/resy_notifier.git
   cd resy_notifier
   ```

2. **Install Dependencies**:
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Setup Database**:
   - Ensure your MySQL database has the necessary schema and tables. Refer to the `db_migrations` directory for SQL scripts.

4. **Configure `.env`**:
   - Create a `.env` file in the root directory:
     ```plaintext
     BASE_URL=https://api.resy.com/4
     ```

---

## Usage

Run the script via the command line:

### Basic Usage
```bash
python main.py <venue_url_name>
```
- `<venue_url_name>`: The URL-friendly name of the restaurant (e.g., `una-pizza-napoletana`).

### Advanced Usage
```bash
python main.py <venue_url_name> [party_size] [start_date] [end_date] [request_interval]
```

| Parameter          | Description                                                                 | Default         |
|--------------------|-----------------------------------------------------------------------------|-----------------|
| `venue_url_name`   | The URL-friendly name of the venue.                                         | **Required**    |
| `party_size`       | Number of guests for the reservation.                                       | `2`             |
| `start_date`       | Start date for checking availability (format: `YYYY-MM-DD`).               | Today           |
| `end_date`         | End date for checking availability (format: `YYYY-MM-DD`).                 | Today + 14 days |
| `request_interval` | Interval (in seconds) between API requests.                                | `60`            |

### Example
```bash
python main.py una-pizza-napoletana 4 2024-12-01 2024-12-07 900
```
- **Venue**: Una Pizza Napoletana
- **Party Size**: 4
- **Date Range**: 2024-12-01 to 2024-12-07
- **Request Interval**: 15 minutes

---

## How It Works

1. **Initialization**:
   - Retrieves the active API key and venue details from the MySQL database.

2. **API Requests**:
   - Queries the Resy API for availability.

3. **Email Notifications**:
   - Sends a single email summarizing available slots when detected.

4. **Polling**:
   - Repeats the request at the specified interval until availability is found.

---

## Troubleshooting

### Common Errors
- **Invalid API Key**:
  Ensure your database has a valid API key, or check the `.env` configuration.
- **Invalid Party Size**:
  Ensure you provide a numeric value for the party size.
- **Database Connection Errors**:
  Verify your MySQL server credentials and connection settings.
