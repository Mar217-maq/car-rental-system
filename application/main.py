import os
import sys

# Set the working directory to the project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

import time

from datetime import datetime
from tabulate import tabulate
from decouple import config
from application.user_management import UserManagement
from application.car_management import CarManagement
from application.rental_booking import RentalBooking
from application.rental_management import RentalManagement
from database.db_connection import DatabaseConnection
from application.config import DatabaseConfig
from data_models.car import Car

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()

def main():
    try:
        # Initialize DatabaseConnection
        db_connection = DatabaseConnection(DatabaseConfig)
        db_connection.ping()  # Ensure the connection is alive

        # Initialize services with the database connection
        user_management = UserManagement(db_connection)
        car_management = CarManagement(db_connection)
        rental_booking = RentalBooking(db_connection)
        rental_management = RentalManagement(db_connection)

        while True:
            clear_screen()
            print("\n============================================")
            print("\tWelcome to Car Rental System")
            print("============================================")
            print("1. Register")
            print("2. Login")
            print("3. Make Payment")
            print("4. Exit\n")

            option = input("Enter your choice: ")

            if option == "1":
                register_menu(user_management)
            elif option == "2":
                user = login_menu(user_management)
                if user:
                    if user.role == "admin":
                        admin_menu(car_management, rental_management)
                    elif user.role == "customer":
                        customer_menu(rental_booking, user.user_id)

            elif option == "3":
                handle_payment(rental_booking)
            elif option == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

#----------------------register_menu----------------------------
def register_menu(user_management):
    while True:
        clear_screen()
        print("\n--------- Registration Menu --------------\n")
        print("1. Register as Customer")
        print("2. Admin Registration (Restricted)")
        print("3. Go Back\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_customer(user_management)
        elif choice == "2":
            register_admin(user_management)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def register_customer(user_management):
    clear_screen()
    print("\n------------ Register as Customer ------------\n")
    username = input("Enter username: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")

    while True:
        password = input("Enter password: ")
        confirm_password = input("Re-enter your password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    phone_number = input("Enter phone number: ")
    address = input("Enter address: ")

    while True:
        license_number = input("Enter license number: ")
        if license_number.strip():
            break
        else:
            print("License number is required for customers.")

    while True:
        license_expiry_date = input("Enter license expiry date (YYYY-MM-DD): ")
        if license_expiry_date.strip():
            break
        else:
            print("License expiry date is required for customers.")

    role = "customer"
    try:
        user_management.register_user(
            username, password, role, first_name, last_name,
            email, phone_number, address, license_number, license_expiry_date
        )
        print("Customer registration successful!")
        time.sleep(2)  # Wait for 5 seconds

        while True:
            choice = input("Would you like to (1) Login or (2) Exit? Enter 1 or 2:  ").strip().lower()
            if choice == "1":
                handle_login(user_management)
                break
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please enter '1' or '2'.")
    except Exception as e:
        print(f"Registration failed: {e}")


def register_admin(user_management):
    clear_screen()
    print("\n----------- Admin Registration (Restricted) ------------\n")
    admin_code = input("Enter the admin access code: ")

    stored_admin_code = config("ADMIN_SECRET_CODE", default="DEFAULT_ADMIN_CODE")
    if admin_code == stored_admin_code:
        username = input("Enter username: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")

        while True:
            password = input("Enter password: ")
            confirm_password = input("Re-enter your password: ")
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

        phone_number = input("Enter phone number: ")
        address = input("Enter address: ")

        role = "admin"
        try:
            user_management.register_user(
                username, password, role, first_name, last_name,
                email, phone_number, address, None, None
            )
            print("Admin registration successful!")
            time.sleep(2)  # Wait for 2 seconds
            while True:
                choice = input("Would you like to (1) Login or (2) Exit? Enter 1 or 2:  ").strip().lower()
                if choice == "1":
                    handle_login(user_management)
                    break
                elif choice == "2":
                    break
                else:
                    print("Invalid choice. Please enter '1' or '2'.")
        except Exception as e:
            print(f"Admin registration failed: {e}")
    else:
        print("Invalid admin access code. Access denied.")

#---------------------------login_menu-------------------------------------
def login_menu(user_management):
    while True:
        clear_screen()
        print("\n------------- Login -------------\n")
        print("1. Login")
        print("2. Forgot Password")
        print("3. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            user = handle_login(user_management)
            if user:
                return user
        elif choice == "2":
            handle_forgot_password(user_management)
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice, please select a valid option.")


def handle_login(user_management):
    clear_screen()
    print("\n------------- Login -------------\n")
    username = input("Enter username or email: ")
    password = input("Enter password: ")
    try:
        print("Attempting to login...")
        user = user_management.login_user(username, password)
        if user:
            print(f"Login successful. Welcome, {user.username}!")
            time.sleep(2)

            while True:
                choice = input("Would you like to (1) continue or (2) Exit? Enter 1 or 2: ").strip().lower()
                if choice == "1":
                    return user  # Return to main menu or next step
                elif choice == "2":
                    return None  # Exit the login process
                else:
                    print("Invalid choice. Please enter '1' or '2'.")
        else:
            print("Incorrect username or password.\n")
            time.sleep(2)  # Wait for 5 seconds
            while True:
                exit_choice = input("Would you like to exit? (Yes/No): ").strip().lower()
                if exit_choice == "yes":
                    handle_login(user_management)
                elif exit_choice == "no":
                    break  # Retry login
                else:
                    print("Invalid choice. Please enter 'Yes' or 'No'.")
    except Exception as e:
        print(f"Login failed: {e}")
        return None


def handle_forgot_password(user_management):
    clear_screen()
    print("\n------------- Reset Password -------------\n")
    email = input("Enter your registered email: ")

    if user_management.check_user_exists(email):
        reset_token = user_management.set_reset_code(email)
        print(f"A password reset code has been generated: {reset_token}")

        entered_token = input("Enter the reset code: ")
        if user_management.validate_reset_code(email, entered_token):
            new_password = input("Enter your new password: ")
            try:
                user_management.update_password(email, new_password)
                print("Password has been updated successfully.")
                time.sleep(2)  # Wait for 2 seconds
                while True:
                    choice = input("Would you like to (1) continue or (2) Exit? Enter 1 or 2:  ").strip().lower()
                    if choice == "1":
                        handle_login(user_management)
                        break
                    elif choice == "2":
                        break
            except Exception as e:
                print(f"Password update failed: {e}")
        else:
            print("Invalid or expired reset code.")
    else:
        print("Email not found.")
        time.sleep(2)  # Wait for 2 seconds
        while True:
            choice = input("Would you like to (1) Continue or (2) Exit? Enter 1 or 2:  ").strip().lower()
            if choice == "1":
                handle_forgot_password(user_management)
                break
            elif choice == "2":
                break

#---------------------------admin_menu-------------------------------------
def admin_menu(car_management, rental_management):
    while True:
        clear_screen()
        print("\n------------ Admin Menu -----------\n")
        print("1. Add Car")
        print("2. Update Car")
        print("3. Delete Car")
        print("4. View All Cars")
        print("5. Approve Rental Request")
        print("6. Reject Rental Request")
        print("7. Returned Car")
        print("8. Generate Reports")
        print("9. Logout\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_screen()
            add_car(car_management)
        elif choice == "2":
            clear_screen()
            update_car(car_management)
        elif choice == "3":
            clear_screen()
            delete_car(car_management)
        elif choice == "4":
            clear_screen()
            view_all_cars(car_management)
        elif choice == "5":
            clear_screen()
            approve_rental(rental_management)
        elif choice == "6":
            clear_screen()
            reject_rental(rental_management)
        elif choice == "7":
            clear_screen()
            return_car(rental_management)
        elif choice == "8":
            clear_screen()
            generate_reports(rental_management)
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def add_car(car_management):
    while True:
        clear_screen()
        print("\n------------- Add Cars -------------\n")
        make = input("Enter car make: ")
        model = input("Enter car model: ")
        year = int(input("Enter car year: "))
        mileage = int(input("Enter car mileage: ").replace(",", ""))
        available = True
        min_rent_period = int(input("Enter minimum rental period (days): "))
        max_rent_period = int(input("Enter maximum rental period (days): "))

        daily_rate_input = input("Enter daily rental rate: ")
        daily_rate = float(''.join([char for char in daily_rate_input if char.isdigit() or char == '.']) or 0)

        car = Car(
            car_id=None,  # Assuming car_id is auto-generated by the database
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            available_now=available,
            min_rent_period=min_rent_period,
            max_rent_period=max_rent_period,
            daily_rate=daily_rate
        )

        try:
            car_management.add_car(car)
            print(f"{make} {model} car added successfully!")
            time.sleep(2)  # Wait for 2 seconds
            while True:
                choice = input("Would you like to (1) Add Car or (2) Exit? Enter 1 or 2: ").strip().lower()
                if choice == "1":
                    add_car(car_management)
                    break
                elif choice == "2":
                    return
        except Exception as e:
            print(f"Failed to add car: {e}")
            return


def update_car(car_management):
    clear_screen()
    print("\n------------- Update Cars -------------\n")
    car_id = int(input("Enter car ID to update: "))

    # Check if the car ID exists
    car = car_management.get_car_by_id(car_id)
    if not car:
        print(f"Car with ID {car_id} does not exist.")
        time.sleep(2)  # Wait for 2 seconds
        return

    make = input("Enter new car make: ").capitalize()
    model = input("Enter new car model: ").capitalize()
    year = int(input("Enter new car year: "))
    mileage = int(input("Enter new car mileage: ").replace(",", ""))

    while True:
        available_input = input("Is the car available? (yes/no): ").lower()
        if available_input in ["yes", "no"]:
            available = available_input == "yes"
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    min_rent_period = int(input("Enter new minimum rental period (days): "))
    max_rent_period = int(input("Enter new maximum rental period (days): "))

    try:
        car_management.update_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)

        time.sleep(2)  # Wait for 2 seconds
        while True:
            choice = input("Would you like to (1) Update car again or (2) Exit? Enter 1 or 2:  ").strip().lower()
            if choice == "1":
                update_car(car_management)
                break
            elif choice == "2":
                return
    except Exception as e:
        print(f"Failed to update car: {e}")

def delete_car(car_management):
    while True:
        clear_screen()
        print("\n------------- Delete Cars -------------\n")
        car_id = int(input("Enter car ID to delete: "))
        try:
            # Check if the car ID exists
            car = car_management.get_car_by_id(car_id)
            if car:
                car_management.delete_car(car_id)
                print(f"Car with ID {car_id} deleted successfully.")
            else:
                print(f"No car with ID {car_id} exists in the database.")
        except Exception as e:
            print(f"Failed to delete car: {e}")

        time.sleep(2)  # Wait for 2 seconds
        exit_choice = input("Do you want to delete another car (yes/no): ").lower()
        if exit_choice != "yes":
            break  # Exit the loop if the user chooses not to delete another car


def view_all_cars(car_management):
    clear_screen()
    print("\n\t\t\t------------------------------------ View All Cars ----------------------------")
    try:
        cars = car_management.list_all_cars()  # Use a method that retrieves all cars
        if cars:
            table = [
                [
                    car.car_id,
                    car.make,
                    car.model,
                    car.year,
                    car.mileage,
                    "Yes" if car.available_now else "No",  # Convert 0/1 to Yes/No
                    car.min_rent_period,
                    car.max_rent_period,
                    f"NZD {car.daily_rate:,.2f}"  # Format the daily rate
                ]
                for car in cars
            ]
            headers = ["ID", "Make", "Model", "Year", "Mileage", "Available", "Min Rent Period",
                       "Max Rent Period", "Daily Rate"]
            print(tabulate(table, headers, tablefmt="grid"))
            time.sleep(2)  # Wait for 2 seconds
            while True:
                exit_choice = input("Do you want to exit? (Please enter Yes): ").lower()
                if exit_choice == "yes":
                    break
        else:
            print("No cars available.")
    except Exception as e:
        print(f"Failed to list cars: {e}")

def approve_rental(rental_management):
    clear_screen()
    print("\n------------- Approve Rental -------------\n")
    rental_id = int(input("Enter rental ID to approve: "))
    try:
        rental_exists = rental_management.check_rental_exists(rental_id)
        if not rental_exists:
            print(f"Error: Rental ID {rental_id} does not exist.")
        else:
            rental_management.approve_rental(rental_id)
    except Exception as e:
        print(f"Error while approving rental: {e}")
    time.sleep(2)  # Wait for 2 seconds
    while True:
        choice = input("Would you like to (1) Approve another one again or (2) Exit? Enter 1 or 2:  ").strip().lower()
        if choice == "1":
            approve_rental(rental_management)
            break
        elif choice == "2":
            break


def handle_payment(rental_booking):
    clear_screen()
    print("\n------------- Make Payment -------------\n")
    rental_id = input("Enter rental ID: ")
    amount = float(input("Enter amount to be paid: "))

    try:
        rental_booking.initiate_payment(rental_id, amount)
    except Exception as e:
        print(f"Payment failed: {e}")

    while True:
        choice = input("Please enter yes to exit): ").strip().lower()
        if choice == "yes":
            break

def reject_rental(rental_management):
    clear_screen()
    print("\n------------- Reject Rental -------------\n")
    rental_id = int(input("Enter rental ID to reject: "))
    try:
        rental_exists = rental_management.check_rental_exists(rental_id)
        if not rental_exists:
            print(f"Error: Rental ID {rental_id} does not exist.")
        else:
            rental_management.reject_rental(rental_id)
            print("Rental rejected successfully!")
    except Exception as e:
        print(f"Failed to reject rental: {e}")
    time.sleep(2)  # Wait for 2 seconds
    while True:
        choice = input("Do you want to exit? (Please enter yes): ").strip().lower()
        if choice == "yes":
            break

def return_car(rental_management):
    clear_screen()
    print("\n------------- Return Car --------------\n")
    rental_id = int(input("Enter rental ID to return: "))
    return_date_actual = input("Enter actual return date (YYYY-MM-DD): ")
    try:
        result = rental_management.process_return(rental_id, return_date_actual)
        print(f"Car returned successfully! Late Fee: {result['late_fee']}, Comments: {result['comments']}")
        while True:
            time.sleep(2)
            exit_choice = input("Do you want to exit? (Please enter yes): ").lower()
            if exit_choice == "yes":
                break
    except Exception as e:
        print(f"Failed to return car: {e}")


def generate_reports(rental_management):
    clear_screen()
    print("\n------------- Generate Reports -------------\n")
    try:
        reports = rental_management.generate_reports()
        print("\n--- Rental Reports ---")
        if not reports:
            print("No rental reports available.")
        else:
            for report in reports:
                print(report)
                time.sleep(2)
    except Exception as e:
        print(f"Failed to generate reports: {e}")

    while True:
        exit_choice = input("Do you want to exit? (Please enter yes): ").lower()
        if exit_choice == "yes":
            break

def customer_menu(rental_booking, user_id):
    while True:
        clear_screen()
        print("\n------------ Customer Menu -------------\n")
        print("1. View Available Cars")
        print("2. Book a Car")
        print("3. View Rental History")
        print("4. Cancel Booking")
        print("5. Logout\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_screen()
            view_available_cars(rental_booking, user_id)
        elif choice == "2":
            clear_screen()
            book_car(rental_booking, user_id)
        elif choice == "3":
            clear_screen()
            view_rental_history(rental_booking, user_id)
        elif choice == "4":
            clear_screen()
            cancel_booking(rental_booking, user_id)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")



def view_available_cars(rental_booking, user_id):
    try:
        cars = rental_booking.get_available_cars()
        if cars:
            print("\n\t\t\t------------- Available Cars -------------\n")
            table = [
                [car.car_id, car.make, car.model, car.year, car.mileage, car.min_rent_period, car.max_rent_period, f"NZD {car.daily_rate:,.2f}"]
                for car in cars
            ]
            headers = ["ID", "Make", "Model", "Year", "Mileage", "Min Rent Period", "Max Rent Period", "Daily Rate"]
            print(tabulate(table, headers, tablefmt="grid"))
            while True:
                choice = input("Would you like to (1) book a car or (2) Exit? Enter 1 or 2: ").strip().lower()
                if choice == "1":
                    book_car(rental_booking, user_id)
                    break
                elif choice == "2":
                    return
        else:
            print("\n\t\t\t------------- Available Cars -------------\n")
            print("No cars available.")
            while True:
                exit_choice = input("Do you want to exit? (Please enter Yes): ").lower()
                if exit_choice == "yes":
                    break
    except Exception as e:
        print(f"Failed to view available cars: {e}")
        while True:
            exit_choice = input("\nDo you want to exit? (Please enter yes): ").lower()
            if exit_choice == "yes":
                break


def book_car(rental_booking, user_id):
    clear_screen()
    print("\n------------- Book a Car -------------\n")
    car_id = int(input("Enter car ID to book: "))
    current_year = datetime.now().year

    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        try:
            start_year = datetime.strptime(start_date, "%Y-%m-%d").year
            end_year = datetime.strptime(end_date, "%Y-%m-%d").year
            if start_year == current_year and end_year == current_year:
                break
            else:
                print(f"Please enter dates within the current year {current_year}.")
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")

    try:
        total_fee = rental_booking.calculate_fee(car_id, start_date, end_date)
        confirm = input(f"The total fee is {total_fee}. Confirm booking? (yes/no): ").lower()
        if confirm == "yes":
            rental_booking.book_car(user_id, car_id, start_date, end_date, total_fee)
            print("Booking confirmed!")
        else:
            print("Booking cancelled.")

        time.sleep(2)  # Wait for 2 seconds
        while True:
            choice = input("Would you like to (1) book a car again or (2) Exit? Enter 1 or 2: ").strip().lower()
            if choice == "1":
                book_car(rental_booking, user_id)
                break
            elif choice == "2":
                return
    except Exception as e:
        print(f"Failed to book car: {e}")


def view_rental_history(rental_booking, user_id):
    clear_screen()
    try:
        rentals = rental_booking.view_rental_history(user_id)
        if rentals:
            print("\n\t\t-------------- Rental History ---------------\n")
            table = [
                [
                    rental['booking_id'],
                    rental['car_id'],
                    rental['rental_start_date'],
                    rental['rental_end_date'],
                    rental['total_rental_price']
                ]
                for rental in rentals
            ]
            headers = ["Booking ID", "Car ID", "Start Date", "End Date", "Total Fee"]
            print(tabulate(table, headers, tablefmt="grid"))
            time.sleep(2)  # Wait for 2 seconds
            while True:
                exit_choice = input("Do you want to exit? (Please enter Yes): ").lower()
                if exit_choice == "yes":
                    break
        else:
            print("\n\t\t\t-------------- Rental History ---------------\n")
            print("No rental history found.")
            time.sleep(2)  # Wait for 2 seconds
            while True:
                exit_choice = input("Do you want to exit? (Please enter yes): ").lower()
                if exit_choice == "yes":
                    break

    except Exception as e:
        print(f"Failed to view rental history: {e}")


def cancel_booking(rental_booking, user_id):
    clear_screen()
    print("\n------------- Cancel Booking -------------\n")
    rental_id = int(input("Enter rental ID to cancel: "))
    cursor = None  # Initialize cursor to None
    try:
        # Check if the rental ID exists
        query = "SELECT booking_id FROM rental_booking WHERE customer_id = %s AND booking_id = %s"
        cursor = rental_booking.db_connection.cursor()
        cursor.execute(query, (user_id, rental_id))
        result = cursor.fetchone()

        if result:
            rental_booking.cancel_booking(user_id, rental_id)
        else:
            print("No booking found with the given rental ID.")

        time.sleep(2)  # Wait for 2 seconds
        while True:
            exit_choice = input("Do you want to exit? (Please Enter Yes): ").lower()
            if exit_choice == "yes":
                break
    except Exception as e:
        print(f"Failed to cancel booking: {e}")
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    main()