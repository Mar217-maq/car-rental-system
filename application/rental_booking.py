#from database.queries import create_rental, select_available_cars
from data_models.car import Car
from datetime import datetime
from application.payment import Payment

class RentalBooking:
    """
    Handles rental booking logic for customers.
    """

    def __init__(self, db_connection):
        """
        Initialize the RentalManager with a database connection.
        :param db_connection: The database connection object.
        """
        self.db_connection = db_connection
        self.payment = Payment(db_connection)  # Initialize Payment class

    def book_car(self, user_id, car_id, start_date, end_date, total_cost):
        """
        Book a car for a specific user and rental period.
        :param user_id: ID of the user booking the car.
        :param car_id: ID of the car to be booked.
        :param start_date: Start date of the rental (YYYY-MM-DD).
        :param end_date: End date of the rental (YYYY-MM-DD).
        :param total_cost: Total cost of the rental.
        :return: None
        """
        query = """
        INSERT INTO rental_booking (car_id, customer_id, rental_start_date, rental_end_date, total_rental_days, status, total_rental_price)
        VALUES (%s, %s, %s, %s, %s, 'pending', %s)
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                rental_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
                cursor.execute(query, (car_id, user_id, start_date, end_date, rental_days, total_cost))
                conn.commit()
                print("Car booked successfully.")
            except Exception as e:
                print(f"Error while booking car: {e}")

    def get_available_cars(self):
        """
        Retrieve all available cars for booking.
        :return: A list of available cars as Car objects.
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM car_management WHERE available_now = 1")
                cars_data = cursor.fetchall()
                return [
                    Car(
                        car_id=row[0],
                        make=row[1],
                        model=row[2],
                        year=row[3],
                        mileage=row[4],
                        available_now=row[5],
                        min_rent_period=row[6],
                        max_rent_period=row[7],
                        daily_rate=row[8]
                    )
                    for row in cars_data
                ]
            except Exception as e:
                print(f"Error while retrieving available cars: {e}")
                return []

    def view_available_cars(self):
        """
        View all available cars for booking.
        :return: None
        """
        try:
            cars = self.get_available_cars()
            if cars:
                print("\n--- Available Cars ---")
                for car in cars:
                    if car.available_now:
                        print(
                            f"ID: {car.car_id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Mileage: {car.mileage}, Min Rent Period: {car.min_rent_period}, Max Rent Period: {car.max_rent_period}")
            else:
                print("No cars available.")
        except Exception as e:
            print(f"Failed to view available cars: {e}")

    def calculate_fee(self, car_id, start_date, end_date):
        """
        Calculate the total rental fee for a given car and rental period.
        :param car_id: ID of the car to be booked.
        :param start_date: Start date of the rental (YYYY-MM-DD).
        :param end_date: End date of the rental (YYYY-MM-DD).
        :return: Total rental fee.
        """
        query = "SELECT daily_rate FROM car_management WHERE car_id = %s"
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (car_id,))
            result = cursor.fetchone()
            if result:
                daily_rate = result[0]
                return self.calculate_rental_fees(daily_rate, start_date, end_date)
            else:
                raise ValueError(f"Car with ID {car_id} not found.")

    @staticmethod
    def calculate_rental_fees(daily_rate, start_date, end_date, additional_charges=0):
        """
        Calculate the total rental cost.
        :param daily_rate: Daily rental rate for the car.
        :param start_date: Start date of the rental (YYYY-MM-DD).
        :param end_date: End date of the rental (YYYY-MM-DD).
        :param additional_charges: Any additional charges (default 0).
        :return: Total cost of the rental.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        duration = (end - start).days + 1  # Include the start day
        return (daily_rate * duration) + additional_charges

    def view_rental_history(self, user_id):
        query = "SELECT * FROM rental_booking WHERE customer_id = %s"
        cursor = None
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            rentals = cursor.fetchall()
            if rentals:
                return rentals
            else:
                return []
        except Exception as e:
            print(f"Error fetching rental history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def cancel_booking(self, user_id, rental_id):
        query = "DELETE FROM rental_booking WHERE customer_id = %s AND booking_id = %s"
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, (user_id, rental_id))
            self.db_connection.commit()
            print("Booking cancelled successfully.")
        except Exception as e:
            print(f"Error cancelling booking: {e}")
        finally:
            if cursor:
                cursor.close()

    def initiate_payment(self, rental_id, amount):
        """
        Initiate the payment process for a rental.
        :param rental_id: The ID of the rental.
        :param amount: The amount to be paid.
        :return: None
        """
        if self.payment.process_payment(rental_id, amount):
            print("Payment successful. Rental confirmed.")
        else:
            print("Payment failed. Please try again.")