import unittest
from model.availability import Availability, Inventory, parse_response

class TestAvailability(unittest.TestCase):
    def setUp(self):
        # Create Inventory instances
        self.inventory_1 = Inventory(reservation="5", event="2", walk_in="3")
        self.inventory_2 = Inventory(reservation="10", event="0", walk_in="1")

        # Create Availability instances
        self.availability_1 = Availability(date="2024-12-01", inventory=self.inventory_1)
        self.availability_2 = Availability(date="2024-12-02", inventory=self.inventory_2)

        # Valid mock API response
        self.valid_data = {
            "scheduled": [
                {
                    "date": "2024-12-01",
                    "inventory": {
                        "reservation": "5",
                        "event": "2",
                        "walk-in": "3",
                    },
                },
                {
                    "date": "2024-12-02",
                    "inventory": {
                        "reservation": "10",
                        "event": "0",
                        "walk-in": "1",
                    },
                },
            ]
        }

        # Invalid mock API responses
        self.invalid_data_missing_scheduled = {}
        self.invalid_data_missing_inventory = {
            "scheduled": [{"date": "2024-12-01"}]
        }
        self.invalid_data_missing_date = {
            "scheduled": [{"inventory": {}}]
        }

    def test_inventory_repr(self):
        # Test the __repr__ method of Inventory
        repr_1 = repr(self.inventory_1)
        repr_2 = repr(self.inventory_2)

        expected_repr_1 = "Inventory(reservation=5, event=2, walk_in=3)"
        expected_repr_2 = "Inventory(reservation=10, event=0, walk_in=1)"

        self.assertEqual(repr_1, expected_repr_1)
        self.assertEqual(repr_2, expected_repr_2)

    def test_availability_repr(self):
        # Test the __repr__ method of Availability
        repr_1 = repr(self.availability_1)
        repr_2 = repr(self.availability_2)

        expected_repr_1 = "Availability(date=2024-12-01, inventory=Inventory(reservation=5, event=2, walk_in=3))"
        expected_repr_2 = "Availability(date=2024-12-02, inventory=Inventory(reservation=10, event=0, walk_in=1))"

        self.assertEqual(repr_1, expected_repr_1)
        self.assertEqual(repr_2, expected_repr_2)

    def test_parse_response_valid(self):
        # Test parsing of a valid response
        result = parse_response(self.valid_data)

        # Expected parsed result
        expected_result = [
            self.availability_1,
            self.availability_2
        ]

        self.assertEqual(len(result), len(expected_result))
        for res, exp in zip(result, expected_result):
            self.assertEqual(res.date, exp.date)
            self.assertEqual(res.inventory.reservation, exp.inventory.reservation)
            self.assertEqual(res.inventory.event, exp.inventory.event)
            self.assertEqual(res.inventory.walk_in, exp.inventory.walk_in)

    def test_parse_response_missing_scheduled_key(self):
        # Test response with missing 'scheduled' key
        with self.assertRaises(ValueError) as context:
            parse_response(self.invalid_data_missing_scheduled)
        self.assertEqual(
            str(context.exception), "Invalid response format: 'scheduled' key missing."
        )

    def test_parse_response_missing_date(self):
        # Test response with missing keys in 'scheduled' entries
        with self.assertRaises(ValueError) as context:
            parse_response(self.invalid_data_missing_date)
        self.assertEqual(
            str(context.exception),
            "Invalid response format: Missing 'date' or 'inventory' key.",
        )

    def test_parse_response_missing_inventory(self):
        # Test response with missing keys in 'scheduled' entries
        with self.assertRaises(ValueError) as context:
            parse_response(self.invalid_data_missing_inventory)
        self.assertEqual(
            str(context.exception),
            "Invalid response format: Missing 'date' or 'inventory' key.",
        )


if __name__ == "__main__":
    unittest.main()
