import mysql.connector

class Payment:
    """
    Handles payment processing for car rentals.
    """

    def __init__(self, db_connection):
        """
        Initialize the Payment class with a database connection.
        :param db_connection: The database connection object.
        """
        self.db_connection = db_connection

    def process_payment(self, rental_id, amount):
        query = """
        UPDATE rental_booking 
        SET payment_status = 'paid', amount_paid = %s, status = 'confirmed' 
        WHERE booking_id = %s
        """
        with self.db_connection.connect() as conn:
            cursor = conn.cursor()
            try:
                # Ensure rental_id and amount are valid
                rental_id = int(rental_id)
                amount = float(amount)

                # Execute the query
                cursor.execute(query, (amount, rental_id))
                conn.commit()
                print("Payment processed successfully.")
                return True
            except ValueError:
                print("Invalid rental_id or amount type")
                return False
            except mysql.connector.Error as db_err:
                print(f"Database error processing payment: {db_err}")
                return False
            except Exception as e:
                print(f"Error processing payment: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()