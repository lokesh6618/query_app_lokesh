import unittest
import pandas as pd

from src.db_connect import DbConnect

class TestDbConnect(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a test database connection."""
        self.db = DbConnect()
        self.table_name = "test_table"
        self.headers = ["id INT", "name VARCHAR(255)"]

    def test_is_table_exists(self) -> None:
        """Test that is_table_exists returns False for a non-existing table."""
        table_name = "random_table"
        self.assertFalse(self.db.is_table_exists(table_name))

    def test_create_table(self) -> None:
        """Test table creation in the database."""
        self.db.create_table(self.table_name, self.headers)
        self.assertTrue(self.db.is_table_exists(self.table_name))

    def test_add_data_from_dataframe(self) -> None:
        """Test adding data from DataFrame to the database."""
        self.db.create_table(self.table_name, self.headers)
        self.assertTrue(self.db.is_table_exists(self.table_name))

        df = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
        self.db.add_data_from_data_frame(self.table_name, df)

        result = self.db.fetch_data_by_id(self.table_name, 1)
        self.assertEqual(result[1], "A")

    def test_drop_table(self) -> None:
        """Test that a table can be created and then dropped successfully."""
        table_name = "drop_table"
        headers = ["id INT", "name VARCHAR(255)"]

        self.db.create_table(table_name, headers)
        self.assertTrue(self.db.is_table_exists(table_name))

        self.db.drop_table(table_name)
        self.assertFalse(self.db.is_table_exists(table_name))

    def tearDown(self) -> None:
        """Clean up after each test."""
        if self.db.is_table_exists(self.table_name):
            self.db.drop_table(self.table_name)

        self.db.close_connector()


if __name__ == "__main__":
    unittest.main()
