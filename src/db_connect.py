import pandas as pd
import psycopg2
from psycopg2 import sql
from typing import List, Optional

from .data_parser import generate_header_from_dataframe

def get_column_name_from_header(table_header: List[str]) -> List[str]:
    """
    Extracts and returns the table names from a list of table headers.
    Args:
        table_header (List[str]): A list of table headers as strings.
    Returns:
        List[str]: A list of extracted table names.
    """
    return [item.split('" ')[0].strip('"') for item in table_header]

class DbConnect:
    """Class to manage PostgreSQL database connections and operations."""

    def __init__(self) -> None:
        """Initialize database connection parameters and establish a connection."""
        self.db_name = "postgres"
        self.user = "postgres"
        self.password = "123456"
        self.host = "localhost"
        self.port = "5432"
        self.connector = None

        self._get_connector()

    def _get_connector(self) -> None:
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connector = psycopg2.connect(
                dbname=self.db_name, 
                user=self.user, 
                password=self.password, 
                host=self.host, 
                port=self.port
            )

        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close_connector(self) -> None:
        """Close the database connection."""
        if self.connector:
            self.connector.close()

    def is_connected(self) -> bool:
        """
        Check if the database connection is still active.
        Returns:
            bool: True if the connection is active, False otherwise.
        """
        return self.connector is not None and self.connector.closed == 0

    def create_table(self, table_name: str, table_headers: List[str]) -> None:
        """
        Create a table in the database.
        Args:
            table_name (str): Name of the table to be created.
            table_headers (list): List of column definitions for the table.
        """
        if not self._is_valid_keyword(table_name):
            raise ValueError(f"Invalid table name: {table_name}")

        for header in get_column_name_from_header(table_headers):
            if not self._is_valid_keyword(header):
                raise ValueError(f"Invalid column name: {header}")

        create_table_query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS {table} ({fields})"
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.SQL, table_headers))
        )

        try:
            self._get_connector()

            cur = self.connector.cursor()
            cur.execute(create_table_query)
            self.connector.commit()

        except Exception as e:
            print(f"Error while creating table: {e}")
            if self.connector:
                self.connector.rollback()

        finally:
            if self.connector:
                cur.close()
                self.connector.close()

    def is_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database.
        Args:
            table_name (str): The name of the table to check.
        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables 
            WHERE table_name = %s
        );
        """
        try:
            self._get_connector()

            cur = self.connector.cursor()
            cur.execute(query, (table_name,))
            exists = cur.fetchone()[0]
            return exists
        except Exception as e:
            print(f"Error checking table existence: {e}")
            return False
        finally:
            if self.connector:
                self.close_connector()

    def add_data_from_data_frame(self, table_name: str, data_frame: pd.DataFrame) -> None:
        """
        Insert data from a DataFrame into the specified table.
        Args:
            table_name (str): Name of the table to insert data into.
            data_frame (pd.DataFrame): DataFrame containing the data to insert.
        """
        try:
            table_header = generate_header_from_dataframe(data_frame)

            if not self.is_table_exists(table_name):
                self.create_table(table_name, table_header)

            if not self.is_connected():
                self._get_connector()

            cur = self.connector.cursor()

            if not self._is_valid_keyword(table_name):
                raise ValueError(f"Invalid table name: {table_name}")

            columns = list(data_frame.columns)
            columns_sql = sql.SQL(', ').join(map(sql.Identifier, columns))
            placeholders = sql.SQL(', ').join(sql.Placeholder() * len(columns))

            final_query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
                table=sql.Identifier(table_name),
                fields=columns_sql,
                values=placeholders
            )

            for _, row in data_frame.iterrows():
                cur.execute(final_query, tuple(row))

            self.connector.commit()

        except Exception as e:
            print(f"Error while adding data from data frame: {e}")
            if self.connector:
                self.connector.rollback()

        finally:
            if self.connector:
                self.connector.close()

    def drop_table(self, table_name: str) -> None:
        """Drop a table from the database by its name.
        Args:
            table_name (str): The name of the table to drop.
        Raises:
            Exception: If there is an error during the table drop operation.
        """
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"

        try:
            self._get_connector()
            cur = self.connector.cursor()
            cur.execute(drop_table_query)
            self.connector.commit()
        except Exception as e:
            print(f"Error dropping table '{table_name}': {e}")
            if self.connector:
                self.connector.rollback()
        finally:
            if self.connector:
                self.close_connector()

    def fetch_data_by_id(self, table_name: str, record_id: int) -> tuple:
        """Fetch a row from the specified table where the 'id' column 
           matches the provided record ID.
        Args:
            table_name (str): The name of the table to query.
            record_id (int): The ID of the record to fetch.
        Returns:
            tuple: The row data that matches the ID, or None if not found.
        """
        query = f"SELECT * FROM {table_name} WHERE id = %s;"

        try:
            self._get_connector()
            cur = self.connector.cursor()
            cur.execute(query, (record_id,))
            result = cur.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching data by ID: {e}")
            return None
        finally:
            if self.connector:
                self.close_connector()

    def run_custom_query(self, query: str, values: tuple) -> Optional[tuple]:
        """Execute a custom query on the database and return a single result.
        Args:
            query (str): The SQL query to execute.
            values (tuple): The parameters to bind to the query.
        Returns:
            tuple | None: The fetched result as a tuple if successful, 
                        or None if an error occurs.
        """
        try:
            self._get_connector()
            cur = self.connector.cursor()
            cur.execute(query, values)
            result = cur.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching data by ID: {e}")
            return None
        finally:
            if self.connector:
                self.close_connector()

    def _is_valid_keyword(self, name: str) -> bool:
        """Checks if the provided name is a reserved SQL keyword 
        (e.g., SELECT, DROP, INSERT, DELETE).
        Args:
            name (str): The name to check.
        Returns:
            bool: True if the name is a reserved SQL keyword, False otherwise.
        """
        return not name.upper() in {'SELECT', 'DROP', 'INSERT', 'DELETE'}
