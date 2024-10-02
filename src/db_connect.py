import pandas as pd
import psycopg2
from typing import List, Optional

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