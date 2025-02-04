from database.queries import get_pending_rentals, approve_rental # update_rental_record, get_rental_details
from data_models.rental import Rental
from datetime import datetime


class RentalManagement:
    """
    Handles rental management logic for admin operations.
    """

    def __init__(self, db_connection):
        """
        Initialize the RentalAdminManager with a database connection.
        :param db_connection: The database connection object.
        """
        self.db_connection = db_connection

    def get_pending_rentals(self):
        """
        Retrieve all pending rental requests.
        :return: A list of Rental objects for pending requests.
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(get_pending_rentals)
                rentals_data = cursor.fetchall()
                return [
                    Rental(
                        rental_id=row[0],
                        user_id=row[1],
                        car_id=row[2],
                        start_date=row[3],
                        end_date=row[4],
                        total_cost=row[5],
                        status=row[6],
                    )
                    for row in rentals_data
                ]
            except Exception as e:
                print(f"Error while retrieving pending rentals: {e}")
                return []

    def check_rental_exists(self, rental_id):
        query = "SELECT 1 FROM rental_booking WHERE booking_id = %s"
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (rental_id,))
            return cursor.fetchone() is not None


    def approve_rental(self, rental_id):
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                # Check if the rental ID exists
                cursor.execute("SELECT car_id FROM rental_booking WHERE booking_id = %s", (rental_id,))
                result = cursor.fetchone()
                if not result:
                    print(f"Error: Rental ID {rental_id} does not exist.")
                    return

                car_id = result[0]

                # Approve the rental if it exists
                cursor.execute(
                    "UPDATE rental_booking SET status = 'confirmed' WHERE booking_id = %s",
                    (rental_id,)
                )

                # Update the car's availability status
                cursor.execute(
                    "UPDATE car_management SET available_now = 0 WHERE car_id = %s",
                    (car_id,)
                )

                conn.commit()
                print(f"Rental ID {rental_id} approved successfully.")
            except Exception as e:
                print(f"Error while approving rental: {e}")

    def reject_rental(self, rental_id):
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE rental_booking SET status = 'cancelled' WHERE booking_id = %s", (rental_id,))
                conn.commit()
                print(f"Rental ID {rental_id} rejected successfully.")
            except Exception as e:
                print(f"Error while rejecting rental: {e}")

    def generate_reports(self):
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM rental_management")
                reports = cursor.fetchall()
                if not reports:
                    print("No rental reports available.")
                    return []
                return reports
            except Exception as e:
                print(f"Failed to generate reports: {e}")
                return []


    def update_rental_status(self, rental_id, status):
        """
        Update the status of a rental request.
        :param rental_id: The ID of the rental request.
        :param status: New status ('Approved' or 'Rejected').
        :return: None
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(approve_rental, (status, rental_id))
                conn.commit()
                print(f"Rental ID {rental_id} updated to '{status}'.")
            except Exception as e:
                print(f"Error while updating rental status: {e}")

    def calculate_late_fee(self, rental_id, return_date_actual):
        """
        Calculate the late fee for a rental based on the return date.
        :param rental_id: The ID of the rental.
        :param return_date_actual: The actual return date.
        :return: The late fee amount.
        """
        # Fetch rental details
        query = "SELECT end_date, car_id FROM rentals WHERE rental_id = %s"

        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (rental_id,))
            rental = cursor.fetchone()

        if not rental:
            raise ValueError(f"Rental with ID {rental_id} not found.")

        end_date = rental['end_date']
        car_id = rental['car_id']

        # Convert dates to datetime objects
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            return_date_actual_obj = datetime.strptime(return_date_actual, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format for return date.")

        # Calculate late days if the return is later than the due date
        if return_date_actual_obj > end_date_obj:
            late_days = (return_date_actual_obj - end_date_obj).days

            # Fetch daily rate for the car
            query_car = "SELECT daily_rate FROM cars WHERE car_id = %s"
            car = self.db_connection.fetch_one(query_car, (car_id,))
            daily_rate = car['daily_rate']

            # Apply a late fee rate (e.g., 1.5x the daily rate)
            late_fee = late_days * daily_rate * 1.5
            return late_fee
        else:
            return 0.0

    def process_return(self, rental_id, return_date_actual):
        """
        Process the return of a rental and calculate the late fee if applicable.
        :param rental_id: The ID of the rental.
        :param return_date_actual: The actual return date (YYYY-MM-DD).
        :return: A dictionary with late fee and comments.
        """
        # Fetch rental details
        query = "SELECT rental_end_date, total_rental_price FROM rental_booking WHERE booking_id = %s"
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (rental_id,))
            rental = cursor.fetchone()

        if not rental:
            raise ValueError(f"Rental with ID {rental_id} not found.")

        rental_end_date = rental[0]
        total_rental_price = rental[1]

        # Convert dates to datetime objects
        return_date_actual_obj = datetime.strptime(return_date_actual, "%Y-%m-%d").date()

        # Calculate late days and late fee
        late_days = (return_date_actual_obj - rental_end_date).days
        late_fee = 0
        comments = "Return on time"

        if late_days > 0:
            late_fee = late_days * float(total_rental_price) * 0.15
            comments = f"Late by {late_days} days"

        # Update the rental record in rental_management table
        update_query = """
            UPDATE rental_management
            SET return_date = %s, late_returns_fee = %s, status = 'returned'
            WHERE booking_id = %s
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(update_query, (return_date_actual, late_fee, rental_id))
            conn.commit()

        # Update the payment status and amount paid in rental_booking table
        update_payment_query = """
            UPDATE rental_booking
            SET payment_status = 'paid', amount_paid = total_rental_price + %s
            WHERE booking_id = %s
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(update_payment_query, (late_fee, rental_id))
            conn.commit()

        return {"late_fee": late_fee, "comments": comments}