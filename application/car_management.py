from database.queries import add_car, select_available_cars, update_car, delete_car
from data_models.car import Car

class CarManagement:
    """
    Manages car-related operations such as adding, updating, and retrieving cars.
    """

    def __init__(self, db_connection):
        """
        Initializes the CarManager with a database connection.

        :param db_connection: The database connection object.
        """
        self.db_connection = db_connection

    def add_car(self, car):
        """
        Adds a new car to the system.

        :param car: A Car object containing the car details.
        :return: None
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    add_car,
                    (car.make, car.model, car.year, car.mileage, car.available_now, car.min_rent_period,
                     car.max_rent_period, car.daily_rate),
                )
                conn.commit()

        except Exception as e:
            print(f"Error while adding car: {e}")

    def get_available_cars(self):
        """
        Retrieves all available cars from the system.

        :return: A list of Car objects for available cars.
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(select_available_cars)
                cars_data = cursor.fetchall()
                cars = [
                    Car(
                        car_id=row[0],
                        make=row[1],
                        model=row[2],
                        year=row[3],
                        mileage=row[4],
                        available_now=row[5],
                        min_rent_period=row[6],
                        max_rent_period=row[7],
                        daily_rate=row[8],
                    )
                    for row in cars_data
                ]
                return cars
        except Exception as e:
            print(f"Error while retrieving cars: {e}")
            return []

    def get_car_by_id(self, car_id):
        """
        Retrieves a car by its ID.

        :param car_id: The ID of the car to retrieve.
        :return: A Car object if found, None otherwise.
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM car_management WHERE car_id = %s", (car_id,))
                car_data = cursor.fetchone()
                if car_data:
                    return Car(
                        car_id=car_data[0],
                        make=car_data[1],
                        model=car_data[2],
                        year=car_data[3],
                        mileage=car_data[4],
                        available_now=car_data[5],
                        min_rent_period=car_data[6],
                        max_rent_period=car_data[7],
                        daily_rate=car_data[8]
                    )
                return None
        except Exception as e:
            print(f"Error while retrieving car: {e}")
            return None

    def update_car(self, car_id, make, model, year, mileage, available, min_rent_period, max_rent_period):
        """
        Updates the details of an existing car.

        :param car_id: The ID of the car to be updated.
        :param make: The new make of the car.
        :param model: The new model of the car.
        :param year: The new year of the car.
        :param mileage: The new mileage of the car.
        :param available: The new availability status of the car.
        :param min_rent_period: The new minimum rental period for the car.
        :param max_rent_period: The new maximum rental period for the car.
        :return: None
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(update_car,
                               (make, model, year, mileage, available, min_rent_period, max_rent_period, car_id))
                conn.commit()
                print(f"Car with ID {car_id} updated successfully.")
        except Exception as e:
            print(f"Error while updating car: {e}")

    def delete_car(self, car_id):
        """
        Deletes a car from the system after deleting related rental bookings.

        :param car_id: The ID of the car to be deleted.
        :return: None
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                # Delete related rental bookings first
                cursor.execute("DELETE FROM rental_booking WHERE car_id = %s", (car_id,))
                # Now delete the car
                cursor.execute(delete_car, (car_id,))
                conn.commit()

        except Exception as e:
            print(f"Error while deleting car: {e}")

    def list_cars(self):
        """
        Lists all available cars in the system.

        :return: A list of Car objects for available cars.
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(select_available_cars)
                cars_data = cursor.fetchall()
                cars = [
                    Car(
                        car_id=row[0],
                        make=row[1],
                        model=row[2],
                        year=row[3],
                        mileage=row[4],
                        available_now=row[5],
                        min_rent_period=row[6],
                        max_rent_period=row[7],
                        daily_rate=row[8],
                    )
                    for row in cars_data
                ]
                return cars
        except Exception as e:
            print(f"Error while retrieving cars: {e}")
            return []

    def list_all_cars(self):
        """
        Lists all cars in the system, regardless of availability.

        :return: A list of Car objects for all cars.
        """
        try:
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM car_management")
                cars_data = cursor.fetchall()
                cars = [
                    Car(
                        car_id=row[0],
                        make=row[1],
                        model=row[2],
                        year=row[3],
                        mileage=row[4],
                        available_now=row[5],
                        min_rent_period=row[6],
                        max_rent_period=row[7],
                        daily_rate=row[8],
                    )
                    for row in cars_data
                ]
                return cars
        except Exception as e:
            print(f"Error while retrieving cars: {e}")
            return []