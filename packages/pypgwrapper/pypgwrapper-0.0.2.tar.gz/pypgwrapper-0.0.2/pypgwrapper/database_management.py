import psycopg2
from psycopg2 import sql
import logging
from tabulate import tabulate

class DatabaseManagement():
    def __init__(self, connection, logger: logging.Logger):
        self.connection = connection
        self.logger = logger

    def create_database(self, new_database):
        if self.connection.get_dsn_parameters()["dbname"] != "postgres":
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres", _print_message=False)
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_database))
        self.execute_query(query)
        self.connect(database=current_database, _print_message=False)  # Connect to the new database
        self.logger.info(f"Database '{new_database}' created")

    def delete_database(self, database_to_delete):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres", _print_message=False)
            query = sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(database_to_delete)
            )
            self.execute_query(query)
            self.logger.info(f"Database '{database_to_delete}' deleted")
            self.connect(database=current_database, _print_message=False)
        except psycopg2.Error as e:
            self.logger.error(f"Error deleting database '{database_to_delete}': {e}")
            raise

    def create_user(self, username, password, is_superuser=False):
        query = sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
            sql.Identifier(username), sql.Literal(password)
        )
        if is_superuser:
            query += sql.SQL(" SUPERUSER")
        if self.execute_query(query):
            self.logger.info(f"User '{username}' created")

    def switch_user(self, user, password):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.disconnect(_print_message=False)
            self.user = user
            self.password = password
            self.connect(database=current_database, _print_message=False)
            self.logger.info(f"Switched to user '{user}'")
        except psycopg2.Error as e:
            self.logger.error(f"Error switching to user '{user}': {e}")

    def delete_user(self, username):
        query = sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(username))
        if self.execute_query(query):
            self.logger.info(f"User '{username}' deleted")

    def create_table(self, name, schema):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(name),
            sql.SQL(', ').join(
                sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(data_type)) for col, data_type in schema.items()
            )
        )
        if self.execute_query(query):
            self.logger.info(f"Table '{name}' created")
        else:
            self.logger.error(f"Failed to create table '{name}'")

    def drop_table(self, name):
        query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(name))
        self.execute_query(query)
        self.logger.info(f"Table '{name}' dropped")

    def get_table_schema(self, table):
        try:
            # Use sql.Identifier to safely quote the table name
            query = sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = {}").format(sql.Literal(table))
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                schema = cursor.fetchall()
            # Print table schema using tabulate
            print(tabulate(schema, headers=['Column Name', 'Data Type'], tablefmt='psql'))
        except psycopg2.Error as e:
            self.logger.error(f"Error retrieving schema for table '{table}': {e}")
            raise

    def get_connection_details(self):
        if self.connection:
            self.logger.info(
                f"Connected to database '{self.connection.get_dsn_parameters()['dbname']}' as user '{self.user}'"
            )
        else:
            self.logger.warning("Not connected to any database.")

    def execute_query(self, query, commit=True):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if commit:
                    self.connection.commit()
                return True
        except psycopg2.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise
