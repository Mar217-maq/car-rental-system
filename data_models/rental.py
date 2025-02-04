from datetime import datetime

class Rental:
    LATE_FEE_RATE = 20  # Late fee per day

    def __init__(self, rental_id, user_id, car_id, start_date, end_date, total_cost, status, expected_return_date=None, actual_return_date=None, base_fee=None):
        """
        Initializes the Rental object.

        :param rental_id: The unique identifier for the rental.
        :param user_id: The ID of the user renting the car.
        :param car_id: The ID of the car being rented.
        :param start_date: The start date of the rental (YYYY-MM-DD).
        :param end_date: The end date of the rental (YYYY-MM-DD).
        :param total_cost: The total cost of the rental.
        :param status: The status of the rental ('Pending', 'Approved', 'Rejected').
        :param expected_return_date: The expected return date of the car (YYYY-MM-DD).
        :param actual_return_date: The actual return date of the car (YYYY-MM-DD).
        :param base_fee: The base fee of the rental.
        """
        self.rental_id = rental_id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)
        self.total_cost = total_cost
        self.status = status
        self.expected_return_date = expected_return_date
        self.actual_return_date = actual_return_date
        self.base_fee = base_fee

    def __repr__(self):
        return f"<Rental {self.rental_id}, Status: {self.status}, Total Cost: ${self.total_cost:.2f}>"

    def rental_duration(self):
        """Calculates the rental duration in days."""
        return (self.end_date - self.start_date).days + 1

    def approve(self):
        """Approves the rental request."""
        if self.status == "Pending":
            self.status = "Approved"
        else:
            raise ValueError("Only 'Pending' rentals can be approved.")

    def reject(self):
        """Rejects the rental request."""
        if self.status == "Pending":
            self.status = "Rejected"
        else:
            raise ValueError("Only 'Pending' rentals can be rejected.")

    def is_pending(self):
        """Checks if the rental is pending approval."""
        return self.status == "Pending"

    def is_approved(self):
        """Checks if the rental is approved."""
        return self.status == "Approved"

    def is_rejected(self):
        """Checks if the rental is rejected."""
        return self.status == "Rejected"

    def to_dict(self):
        """Converts the Rental object to a dictionary."""
        return {
            "rental_id": self.rental_id,
            "user_id": self.user_id,
            "car_id": self.car_id,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "total_cost": self.total_cost,
            "status": self.status,
            "expected_return_date": self.expected_return_date,
            "actual_return_date": self.actual_return_date,
            "base_fee": self.base_fee,
        }

    @staticmethod
    def from_dict(data):
        """Creates a Rental object from a dictionary."""
        return Rental(
            rental_id=data.get("rental_id"),
            user_id=data.get("user_id"),
            car_id=data.get("car_id"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            total_cost=data.get("total_cost"),
            status=data.get("status"),
            expected_return_date=data.get("expected_return_date"),
            actual_return_date=data.get("actual_return_date"),
            base_fee=data.get("base_fee"),
        )

    @staticmethod
    def _parse_date(date_str):
        """Parses a date string into a datetime object."""
        return datetime.strptime(date_str, "%Y-%m-%d")

    def calculate_late_fee(self):
        """Calculates the late fee based on actual return date and expected return date."""
        if not self.expected_return_date or not self.actual_return_date:
            return 0  # No late fee if dates are not provided
        expected_date = datetime.strptime(self.expected_return_date, "%Y-%m-%d")
        actual_date = datetime.strptime(self.actual_return_date, "%Y-%m-%d")
        late_days = (actual_date - expected_date).days
        return max(late_days * self.LATE_FEE_RATE, 0)  # No fee if not late

    def calculate_total_fee(self):
        """Calculates the total fee (base fee + late fee)."""
        late_fee = self.calculate_late_fee()
        return self.base_fee + late_fee if self.base_fee is not None else late_fee
