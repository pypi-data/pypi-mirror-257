import logging
import psycopg2
from psycopg2 import sql, extras, extensions
from tabulate import tabulate
import csv
import json
import openpyxl
from decimal import Decimal
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Postgres:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.query = None

    def connect(self, database=None, _print_message=True):
        try:
            database = database or self.current_database
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database,
            )
            self.connection.autocommit = True  # Disable transactions
            if _print_message:
                logger.info(f"Connected to database '{database}' as user '{self.user}'")
        except psycopg2.Error as e:
            logger.error(f"Error connecting to database '{database}' as user '{self.user}': {e}")
            raise

    def disconnect(self, _print_message=True):
        if self.connection:
            self.connection.close()
            if _print_message:
                logger.info("Disconnected from database.")

    def select(self, table, columns=None):
        if columns is None:
            columns_str = "*"
        else:
            columns_str = ", ".join(columns)
        
        self.query = self._build_query(columns=columns_str, table=table)
        return self
    
    def where(self, conditions):
        if conditions:
            where_clause = " AND ".join(f"{key} = {value}" for key, value in conditions.items())
            self.query += self._build_where_clause(where_clause)
        return self

    def order(self, columns, asc=False):
        order_by_clause = self._build_order_by_clause(columns, asc)
        self.query += order_by_clause
        return self

    def groupby(self, columns):
        group_by_clause = self._build_group_by_clause(columns)
        self.query += group_by_clause
        return self
    
    def limit(self, limit_value):
        self.query += f" LIMIT {limit_value}"
        return self

    def execute(self):
        if self.query:
            self.sql(self.query)
        else:
            logger.warning("No query to execute.")

    # Other methods...

    def _build_query(
        self, columns="*", table=None, conditions=None, order_by=None, group_by=None
    ):
        query_template = "SELECT {columns} FROM {table}{where_clause}{group_by_clause}{order_by_clause}"
        where_clause = self._build_where_clause(conditions) if conditions else ""
        group_by_clause = self._build_group_by_clause(group_by) if group_by else ""
        order_by_clause = self._build_order_by_clause(order_by) if order_by else ""
        return query_template.format(
            columns=columns,
            table=table,
            where_clause=where_clause,
            group_by_clause=group_by_clause,
            order_by_clause=order_by_clause,
        )

    def _build_where_clause(self, conditions):
        return f" WHERE {conditions}" if conditions else ""

    def _build_order_by_clause(self, columns, asc=False):
        order_direction = "ASC" if asc else "DESC"
        columns_str = ', '.join(columns)
        return f" ORDER BY {columns_str} {order_direction}" if columns else ""

    def _build_group_by_clause(self, columns):
        columns_str = ', '.join(columns)
        return f" GROUP BY {columns_str}" if columns else ""

    def sql(self, query, commit=False, _print_results=True):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if commit:
                    self.connection.commit()
                else:
                    if cursor.description is not None:
                        columns = [desc[0] for desc in cursor.description]
                        result = cursor.fetchall()
                        if result:
                            if _print_results:
                              print(tabulate(result, headers=columns, tablefmt="psql"))
                        else:
                            logger.info("No results found.")
                        return result, columns
                return True
        except psycopg2.Error as e:
            logger.error(f"Error executing query: {e}")
            raise

    def create_database(self, new_database):
        if self.connection.get_dsn_parameters()["dbname"] != "postgres":
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres")
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_database))
        self.sql(query)
        self.connect(database=current_database, _print_message=False)  # Connect to the new database
        logger.info(f"Database '{new_database}' created")

    def execute(self):
        if self.query:
            self.sql(self.query)
        else:
            logger.warning("No query to execute.")

    def delete_database(self, database_to_delete):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres", _print_message=False)
            query = sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(database_to_delete)
            )
            self.sql(query)
            logger.info(f"Database '{database_to_delete}' deleted")
            self.connect(database=current_database, _print_message=False)
        except psycopg2.Error as e:
            logger.error(f"Error deleting database '{database_to_delete}': {e}")
            raise

    def delete_user(self, username):
        query = sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(username))
        if self.sql(query, commit=True):
            logger.info(f"User '{username}' deleted")

    def create_user(self, username, password, is_superuser=False):
        query = sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
            sql.Identifier(username), sql.Literal(password)
        )
        if is_superuser:
            query += sql.SQL(" SUPERUSER")
        if self.sql(query, commit=True):
            logger.info(f"User '{username}' created")

    def create_table(self, name, schema):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(name),
            sql.SQL(', ').join(
                sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(data_type)) for col, data_type in schema.items()
            )
        )
        if self.sql(query):
            logger.info(f"Table '{name}' created")
        else:
            logger.error(f"Failed to create table '{name}'")

    def drop_table(self, name):
        query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(name))
        self.sql(query)
        logger.info(f"Table '{name}' dropped")

    def switch_user(self, user, password):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.disconnect(_print_message=False)
            self.user = user
            self.password = password
            self.connect(database=current_database, _print_message=False)
            logger.info(f"Switched to user '{user}'")
        except psycopg2.Error as e:
            logger.error(f"Error switching to user '{user}': {e}")
            raise

    def get_connection_details(self):
        if self.connection:
            logger.info(
                f"Connected to database '{self.connection.get_dsn_parameters()['dbname']}' as user '{self.user}'"
            )
        else:
            logger.warning("Not connected to any database.")

    def to_csv(self, output_file="output.csv"):
        if self.query:
            result, columns = self.sql(self.query, _print_results=False)
            if result:
                with open(output_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)  # Assuming self.columns contains column names
                    writer.writerows(result)
                logger.info(f"Results exported to {output_file}")
            else:
                logger.info("No results found.")
        else:
            logger.warning("No query to execute.")

    def to_excel(self, output_file="output.xlsx"):
        if self.query:
            result, columns = self.sql(self.query, _print_results=False)
            if result:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(columns)  # Assuming self.columns contains column names
                for row in result:
                    ws.append(row)
                wb.save(output_file)
                logger.info(f"Results exported to {output_file}")
            else:
                logger.info("No results found.")
        else:
            logger.warning("No query to execute.")

    def to_json(self, output_file="output.json"):
        if self.query:
            result, columns = self.sql(self.query, _print_results=False)
            if result:
                json_result = []
                for row in result:
                    json_row = {}
                    for i, value in enumerate(row):
                        column_name = columns[i]
                        json_row[column_name] = float(value) if isinstance(value, Decimal) else value
                    json_result.append(json_row)
                
                with open(output_file, "w") as f:
                    json.dump(json_result, f, indent=4)
                logger.info(f"Results exported to {output_file}")
            else:
                logger.info("No results found.")
        else:
            logger.warning("No query to execute.")

    def to_parquet(self, output_file="output.parquet"):
        result, columns = self.sql(self.query, _print_results=False)
        if result:
            # Create a pyarrow Table
            table_data = []
            for row in result:
                table_data.append(row)
            table = pa.Table.from_pydict({columns[i]: [row[i] for row in table_data] for i in range(len(columns))})

            # Write the Table to Parquet file
            pq.write_table(table, output_file)
            logger.info(f"Results exported to {output_file}")
        else:
            logger.info("No results found.")

    def upload_to_s3(self, bucket_name, format, filename, acl=None, metadata=None):
        # Ensure that the format is one of the supported options
        if format.lower() not in ['csv', 'excel', 'json', 'parquet']:
            logger.error("Unsupported format. Please provide one of the following: csv, excel, json, parquet")
            return

        # Export data to the specified format
        if format.lower() == 'csv':
            self.to_csv(output_file=filename)
        elif format.lower() == 'excel':
            self.to_excel(output_file=filename)
        elif format.lower() == 'json':
            self.to_json(output_file=filename)
        elif format.lower() == 'parquet':
            self.to_parquet(output_file=filename)

        # Upload the file to S3
        s3 = boto3.client('s3')
        try:
            with open(filename, 'rb') as data:
                s3.upload_fileobj(data, bucket_name, filename, ExtraArgs={'ACL': acl, 'Metadata': metadata})
            logger.info(f"File '{filename}' uploaded to bucket '{bucket_name}'")
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise


# Example usage:
if __name__ == "__main__":
    db = Postgres(host="localhost", port="5432", user="postgres", password="password")

    db.connect(database="market_data")

    #db.create_table(name = "test", schema = {"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(255)", "age": "INTEGER"})
    #db.drop_table("test")

    # db.delete_database("test_db")
    # db.create_database("test_db")

    # db.get_connection_details()

    # db.delete_user("test_user")

    # db.create_user(username="test_user", password="test_password", is_superuser=True)

    # db.switch_user(user="test_user", password="test_password")

    # # db.connect(database="market_data")

    # db.select(table="stock_data.gainers", columns="symbol, price").where(
    #     "symbol = 'HOLO'"
    # ).order("symbol", asc=True).execute()

    #db.sql("SELECT symbol, price FROM stock_data.gainers LIMIT 5")

    # Export results to CSV
 
    # Execute query, export results to Excel, and upload to S3 bucket
    db.select(table="stock_data.gainers", columns=["symbol", "price"]).order(["price"], asc=True)
    db.select(table="stock_data.gainers", columns=["symbol", "price"]).groupby(["symbol", "price"]).to_csv(output_file="output.csv")
    db.select(table="stock_data.gainers", columns=["symbol", "price"]).groupby(["symbol", "price"]).to_json(output_file="output.json")
