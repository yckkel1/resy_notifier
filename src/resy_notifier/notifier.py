class ResyNotifier:
    """
    Handles notifications about available reservations.
    Currently supports console notifications.
    """

    @staticmethod
    def notify(reservations):
        """
        Notify the user about available reservations.

        Args:
            reservations (list): A list of reservation details.
        """
        if not reservations:
            print("No reservations available.")
        else:
            print("Available Reservations:")
            for reservation in reservations:
                print(f"- Date: {reservation['date']} (Reservation: {reservation['inventory']['reservation']})")
