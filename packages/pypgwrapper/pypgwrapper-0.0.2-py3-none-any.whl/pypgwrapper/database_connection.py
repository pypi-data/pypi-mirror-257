import psycopg2
import logging

class DatabaseConnection:
    def __init__(self, host, port, user, password, logger: logging.Logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.logger = logger
        self.connection = None

    def connect(self, database=None, _print_message=True):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database,
            )
            self.connection.autocommit = True  # Disable transactions
            if _print_message:
                self.logger.info(f"Connected to database '{database}' as user '{self.user}'")
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to database '{database}' as user '{self.user}': {e}")
            raise

    def disconnect(self, _print_message=True):
        if self.connection:
            self.connection.close()
            if _print_message:
                self.logger.info("Disconnected from database.")