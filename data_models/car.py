# model/
#car.py

class Car:

        def __init__(self, car_id, make, model, year, mileage, available_now, min_rent_period, max_rent_period, daily_rate):
            """
            Initializes the Car object.

            :param car_id: The unique identifier for the car.
            :param make: The manufacturer of the car.
            :param model: The model of the car.
            :param year: The year the car was manufactured.
            :param mileage: The mileage of the car.
            :param available_now: Boolean indicating if the car is currently available.
            :param min_rent_period: The minimum rental period for the car.
            :param max_rent_period: The maximum rental period for the car.
            """
            self.car_id = car_id
            self.make = make
            self.model = model
            self.year = year
            self.mileage = mileage
            self.available_now = available_now
            self.min_rent_period = min_rent_period
            self.max_rent_period = max_rent_period
            self.daily_rate = daily_rate

        def __repr__(self):
            """
            Provides a string representation of the Car object for debugging purposes.

            :return: A string representation of the Car object.
            """
            return f"<Car {self.make} {self.model}, Year: {self.year}, Available: {self.available_now}, Daily Rate: {self.daily_rate}>"

        def is_available(self):
            """
            Checks if the car is currently available for rental.

            :return: True if the car is available, False otherwise.
            """
            return self.available_now

        def to_dict(self):
            """
            Converts the Car object to a dictionary.

            :return: A dictionary representation of the Car object.
            """
            return {
                "car_id": self.car_id,
                "make": self.make,
                "model": self.model,
                "year": self.year,
                "mileage": self.mileage,
                "available_now": self.available_now,
                "min_rent_period": self.min_rent_period,
                "max_rent_period": self.max_rent_period,
                "daily_rate": self.daily_rate
            }

        @staticmethod
        def from_dict(data):
            """
            Creates a Car object from a dictionary.

            :param data: A dictionary containing car data.
            :return: A Car object.
            """
            return Car(
                car_id=data.get("car_id"),
                make=data.get("make"),
                model=data.get("model"),
                year=data.get("year"),
                mileage=data.get("mileage"),
                available_now=data.get("available_now"),
                min_rent_period=data.get("min_rent_period"),
                max_rent_period=data.get("max_rent_period"),
                daily_rate=data.get("daily_rate")
            )
