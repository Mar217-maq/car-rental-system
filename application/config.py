from decouple import config

# Database Configuration
DatabaseConfig = {
    'host': config('DB_HOST', default='localhost'),           # MySQL server location
    'user': config('DB_USER', default='root'),                # Username to connect to MySQL
    'password': config('DB_PASSWORD'),                        # Password for MySQL user
    'database': config('DB_NAME', default='car_rental_system'),  # Database name
    'port': config('DB_PORT', cast=int, default=3306),        # MySQL server port
}

