from datetime import datetime

class Booking:
    """
    Represents a booking in the car rental system.
    """

    def __init__(self, booking_id, user_id, car_id, start_date, end_date, rental_fee, additional_charges, total_cost, status):
        """
        Initializes the Booking object.

        :param booking_id: The unique identifier for the booking.
        :param user_id: The ID of the user making the booking.
        :param car_id: The ID of the car being booked.
        :param start_date: The start date of the booking (YYYY-MM-DD).
        :param end_date: The end date of the booking (YYYY-MM-DD).
        :param rental_fee: The base rental fee per day for the car.
        :param additional_charges: Any additional charges (e.g., insurance, late fees).
        :param total_cost: The total cost of the booking.
        :param status: The status of the booking ('Pending', 'Confirmed', 'Cancelled').
        """
        self.booking_id = booking_id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)
        self.rental_fee = rental_fee
        self.additional_charges = additional_charges
        self.total_cost = total_cost
        self.status = status

    def __repr__(self):
        """
        Provides a string representation of the Booking object for debugging purposes.

        :return: A string representation of the Booking object.
        """
        return f"<Booking {self.booking_id}, Status: {self.status}, Total Cost: ${self.total_cost:.2f}>"

    def calculate_total_cost(self):
        """
        Calculates the total cost of the booking based on rental duration, rental fee, and additional charges.

        :return: The total cost of the booking.
        """
        duration = self.booking_duration()
        self.total_cost = (self.rental_fee * duration) + self.additional_charges
        return self.total_cost

    def booking_duration(self):
        """
        Calculates the booking duration in days.

        :return: The number of days for the booking.
        """
        return (self.end_date - self.start_date).days + 1

    def is_pending(self):
        """
        Checks if the booking is pending approval.

        :return: True if the status is 'Pending', False otherwise.
        """
        return self.status == 'Pending'

    def is_confirmed(self):
        """
        Checks if the booking is confirmed.

        :return: True if the status is 'Confirmed', False otherwise.
        """
        return self.status == 'Confirmed'

    def is_cancelled(self):
        """
        Checks if the booking is cancelled.

        :return: True if the status is 'Cancelled', False otherwise.
        """
        return self.status == 'Cancelled'

    def to_dict(self):
        """
        Converts the Booking object to a dictionary.

        :return: A dictionary representation of the Booking object.
        """
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "car_id": self.car_id,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "rental_fee": self.rental_fee,
            "additional_charges": self.additional_charges,
            "total_cost": self.total_cost,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Booking object from a dictionary.

        :param data: A dictionary containing booking data.
        :return: A Booking object.
        """
        return Booking(
            booking_id=data.get("booking_id"),
            user_id=data.get("user_id"),
            car_id=data.get("car_id"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            rental_fee=data.get("rental_fee"),
            additional_charges=data.get("additional_charges"),
            total_cost=data.get("total_cost"),
            status=data.get("status")
        )

    @staticmethod
    def _parse_date(date_str):
        """
        Parses a date string into a datetime object.

        :param date_str: The date string in 'YYYY-MM-DD' format.
        :return: A datetime object.
        """
        return datetime.strptime(date_str, "%Y-%m-%d")
