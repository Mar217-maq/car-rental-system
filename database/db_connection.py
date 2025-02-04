import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, config):
        if not hasattr(self, 'initialized'):
            self.config = config
            self.connection = None
            self.initialized = True

    def connect(self):
        """Establishes a connection to the database."""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Error: {e}")
            raise

    def cursor(self, dictionary=False):
        """Returns a cursor object for executing queries."""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection.cursor(dictionary=dictionary)

    def commit(self):
        """Commits any changes to the database."""
        if self.connection and self.connection.is_connected():
            self.connection.commit()

    def close(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def reconnect(self):
        """Re-establish the database connection in case of disconnection."""
        if not self.connection or not self.connection.is_connected():
            self.connect()

    def ping(self):
        """Ping the server to check if the connection is alive."""
        try:
            if self.connection and self.connection.is_connected():
                self.connection.ping(reconnect=True)
        except Error as e:
            print(f"Error pinging database: {e}")
            self.reconnect()

    # Context Manager Support
    def __enter__(self):
        """Enter the context and return the connection object."""
        self.connect()  # Ensure the connection is established
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit the context and close the connection."""
        self.close()

    def query(self, sql):
        """Executes a query and reconnects if connection is lost."""
        try:
            self.ping()  # Ensure the connection is alive
            cursor = self.cursor()  # Ensure the connection is active
            cursor.execute(sql)
            return cursor
        except mysql.connector.Error as e:
            if e.errno == 2006:  # MySQL server has gone away
                print("MySQL server has gone away. Reconnecting...")
                self.connect()  # Reconnect to MySQL
                cursor = self.connection.cursor()
                cursor.execute(sql)
                return cursor
            else:
                print(f"Error executing query: {e}")
                raise