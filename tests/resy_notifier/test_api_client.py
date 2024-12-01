from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from api_client import ResyAPIClient
from model.availability import Availability
import httpx

class TestResyAPIClient:
    def setup_method(self):
        self.mock_get_patcher = patch("httpx.get")
        self.mock_get = self.mock_get_patcher.start()

        self.mock_response_data = {
            "scheduled": [
                {
                    "date": "2024-12-01",
                    "inventory": {
                        "reservation": "sold-out",
                        "event": "not available",
                        "walk-in": "not available",
                    },
                },
                {
                    "date": "2024-12-02",
                    "inventory": {
                        "reservation": "sold-out",
                        "event": "not available",
                        "walk-in": "not available",
                    },
                },
            ],
            "last_calendar_day": "2024-12-21",
        }

    def teardown_method(self):
        self.mock_get_patcher.stop()

    def test_get_availability_dynamic_date_success(self):
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.status_code = 200
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        result = client.get_availability(venue_id=12345)

        # Verify the mocked request parameters
        call_args = self.mock_get.call_args[1]["params"]
        expected_start_date = datetime.now().strftime("%Y-%m-%d")
        expected_end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        assert call_args["start_date"] == expected_start_date
        assert call_args["end_date"] == expected_end_date
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Availability)

    def test_get_availability_static_date_success(self):
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.status_code = 200
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        result = client.get_availability(venue_id=12345, start_date="2024-12-01", end_date="2024-12-02")

        # Verify the mocked request parameters
        call_args = self.mock_get.call_args[1]["params"]

        assert call_args["start_date"] == "2024-12-01"
        assert call_args["end_date"] == "2024-12-02"
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Availability)

    def test_missing_api_key(self):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        self.mock_get.return_value = mock_response

        try:
            client = ResyAPIClient(base_url="test_base_url")
            client.get_availability(venue_id=12345)
            assert False, "Expected ValueError for invalid response format."
        except ValueError as e:
            assert "API key is required." in str(e)

    def test_missing_base_url(self):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        self.mock_get.return_value = mock_response

        try:
            client = ResyAPIClient(api_key="test_api_key")
            client.get_availability(venue_id=12345)
            assert False, "Expected ValueError for invalid response format."
        except ValueError as e:
            assert "Base URL is required." in str(e)

    def test_invalid_response_format(self):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        try:
            client.get_availability(venue_id=12345)
            assert False, "Expected ValueError for invalid response format."
        except ValueError as e:
            assert "Error parsing response" in str(e)

    def test_httpx_request_error(self):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.RequestError("Bad Request")
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        try:
            client.get_availability(venue_id=99999)
            assert False, "Expected Network error."
        except ValueError as e:
            assert str(e) == "Network error occurred: Bad Request"

    def test_internal_error(self):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Internal Error", request=None, response=mock_response
        )
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        try:
            client.get_availability(venue_id=99999)
            assert False, "Expected HTTP error."
        except ValueError as e:
            assert str(e) == "HTTP error occurred: Internal Error"

    def test_invalid_venue_id(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=None, response=mock_response
        )
        self.mock_get.return_value = mock_response

        client = ResyAPIClient(api_key="test_api_key", base_url="test_base_url")
        try:
            client.get_availability(venue_id=99999)
            assert False, "Expected ValueError for invalid venue ID."
        except ValueError as e:
            assert str(e) == "Venue ID 99999 not found."
