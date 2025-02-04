import mysql.connector
import bcrypt
from database.queries import create_user
from database.db_connection import DatabaseConnection
import string
import random
from datetime import datetime, timedelta
from data_models.user import User

class UserManagement:
    """
    Manages user-related operations such as registration, login, and password reset.
    """

    def __init__(self, db_connection: DatabaseConnection):
        """
        Initializes the UserManager with a database connection.

        :param db_connection: The database connection object.
        """
        self.db_connection = db_connection

    # -------------------- Reset Token Functionality --------------------

    @staticmethod
    def generate_reset_code():
        """Generate a random 8-character alphanumeric token."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def set_reset_code(self, email):
        """Generate and save a reset token for the user."""
        code = self.generate_reset_code()
        expiry_time = datetime.now() + timedelta(minutes=15)  # Token valid for 15 minutes
        query = """
           UPDATE user_management 
           SET reset_code = %s, reset_code_expiry = %s 
           WHERE email = %s
           """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, (code, expiry_time, email))
            self.db_connection.commit()
            return code
        except Exception as e:
            print(f"Database Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def validate_reset_code(self, email, code):
        """Check if the token is valid for the user."""
        query = """
           SELECT reset_code, reset_code_expiry 
           FROM user_management  
           WHERE email = %s
           """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                reset_code, reset_code_expiry = user  # Accessing via index
                if reset_code == code:
                    if datetime.now() <= reset_code_expiry:  # Fix: Use the variable directly
                        return True
                    else:
                        print("Code expired.")
            return False
        except Exception as e:
            print(f"Error during reset code validation: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_password(self, email, new_password):
        """Update the user's password."""
        query = """
           UPDATE user_management  
           SET password_hash = %s, reset_code = NULL, reset_code_expiry = NULL
           WHERE email = %s
           """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            cursor.execute(query, (password_hash.decode("utf-8"), email))
            self.db_connection.commit()
        except Exception as e:
            print(f"Error during password update: {e}")
        finally:
            if cursor:
                cursor.close()

    # -------------------- User Registration --------------------

    def register_user(
        self,
        username,
        password,
        role,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        license_number,
        license_expiry_date
    ):
        """
        Registers a new user with detailed profile information.
        """
        # Hash the password for secure storage
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Store the hashed password in the database

        # If the user is an admin, set license_number and license_expiry_date to None
        if role == "Admin":
            license_number = None
            license_expiry_date = None

        # Database operation
        cursor = None
        try:
            # Use the context manager for connection handling
            with self.db_connection.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    create_user,
                    (
                        username,
                        password_hash.decode("utf-8"),
                        role,
                        first_name,
                        last_name,
                        email,
                        phone_number,
                        address,
                        license_number,
                        license_expiry_date,
                    ),
                )
                conn.commit()
                print(f"User '{username}' registered successfully.")
        except mysql.connector.Error as e:
            print(f"Error during registration: {e}")
        except Exception as e:
            print(f"Error during registration: {e}")
        finally:
            if cursor:
                cursor.close()

    # -------------------- User Login --------------------

    def login_user(self, username, password):
        cursor = None
        try:
            self.db_connection.ping()
            with self.db_connection.connect() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT user_id, password_hash, role FROM user_management WHERE BINARY username = %s OR BINARY email = %s",
                    (username, username)
                )
                result = cursor.fetchone()
                if result:
                    user_id = result['user_id']
                    stored_password_hash = result['password_hash']
                    role = result['role']
                    if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                        return User(user_id=user_id, username=username, password_hash=stored_password_hash, role=role)
                    else:
                        return None  # Incorrect password
                else:
                    return None  # User does not exist
        except mysql.connector.Error as db_err:
            print(f"Database error during login: {db_err}")
            return None
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # -------------------- Check User Existence --------------------

    def check_user_exists(self, email):
        """Check if a user exists with the given email."""
        query = """
           SELECT user_id
           FROM user_management
           WHERE email = %s
           """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user is not None
        except Exception as e:
            print(f"Error during user existence check: {e}")
            return False
        finally:
            if cursor:
                cursor.close()