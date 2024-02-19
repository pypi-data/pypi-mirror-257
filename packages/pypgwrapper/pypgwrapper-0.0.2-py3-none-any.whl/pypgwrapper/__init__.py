import logging
from .database_connection import DatabaseConnection
from .database_management import DatabaseManagement
from .data_operations import DataOperations

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] [%(name)s] - %(message)s",
)

logger = logging.getLogger(__name__)

class Postgres(DatabaseConnection, DatabaseManagement, DataOperations):
    def __init__(self, host, port, user, password, logger: logging.Logger = logger):
        super().__init__(host, port, user, password, logger)
        self.params = ()

    def connect(self, database=None, _print_message=True):
        super().connect(database)

    def disconnect(self):
        super().disconnect()

    def create_database(self, new_database):
        super().create_database(new_database)

    def delete_database(self, database_to_delete):
        super().delete_database(database_to_delete)

    def create_user(self, username, password, is_superuser=False):
        super().create_user(username, password, is_superuser)

    def delete_user(self, username):
        super().delete_user(username)

    def create_table(self, name, schema):
        super().create_table(name, schema)

    def drop_table(self, name):
        super().drop_table(name)

    def get_table_schema(self, table):
        super().get_table_schema(table)

    def get_connection_details(self):
        super().get_connection_details()

    def execute_query(self, query, commit=True):
        super().execute_query(query, commit)

    # Methods from DataOperations class
    def select(self, table, columns=None):
        return super().select(table, columns)

    def where(self, conditions):
        return super().where(conditions)

    def order(self, columns, asc=False):
        return super().order(columns, asc)

    def groupby(self, columns):
        return super().groupby(columns)

    def limit(self, limit_value):
        return super().limit(limit_value)

    def execute(self):
        super().execute()

    def sql(self, query, commit=False, _print_results=True):
        return super().sql(query, commit, _print_results)

    def to_csv(self, output_file="output.csv"):
        super().to_csv(output_file)

    def to_excel(self, output_file="output.xlsx"):
        super().to_excel(output_file)

    def to_json(self, output_file="output.json"):
        super().to_json(output_file)

    def to_parquet(self, output_file="output.parquet"):
        super().to_parquet(output_file)

    def upload_to_s3(self, bucket_name, format, filename, acl=None, metadata=None):
        super().upload_to_s3(bucket_name, format, filename, acl, metadata)
