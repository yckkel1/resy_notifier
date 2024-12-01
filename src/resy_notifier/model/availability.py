from typing import List


class Inventory:
    """
    Represents the inventory for a specific date.
    """
    def __init__(self, reservation: str, event: str, walk_in: str):
        self.reservation = reservation
        self.event = event
        self.walk_in = walk_in

    def __repr__(self):
        return f"Inventory(reservation={self.reservation}, event={self.event}, walk_in={self.walk_in})"


class Availability:
    """
    Represents availability for a specific date.
    """
    def __init__(self, date: str, inventory: Inventory):
        self.date = date
        self.inventory = inventory

    def __repr__(self):
        return f"Availability(date={self.date}, inventory={self.inventory})"


def parse_response(data: dict) -> List[Availability]:
    """
    Parse the API response JSON into a list of Availability objects.
    """
    # Ensure the response contains 'scheduled'
    if not isinstance(data, dict) or "scheduled" not in data:
        raise ValueError("Invalid response format: 'scheduled' key missing.")

    availability_list = []
    for item in data.get("scheduled", []):
        # Validate inventory keys
        if "inventory" not in item or "date" not in item:
            raise ValueError("Invalid response format: Missing 'date' or 'inventory' key.")
        inventory_data = item.get("inventory", {})
        inventory = Inventory(
            reservation=inventory_data.get("reservation", "unknown"),
            event=inventory_data.get("event", "unknown"),
            walk_in=inventory_data.get("walk-in", "unknown"),
        )
        availability = Availability(date=item["date"], inventory=inventory)
        availability_list.append(availability)
    return availability_list
