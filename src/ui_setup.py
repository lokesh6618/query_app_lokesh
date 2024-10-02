import os

import pandas as pd
from PySide2.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .data_parser import generate_header_from_csv, get_dataframe_from_csv
from .db_connect import DbConnect
from .utils import get_filename_from_filepath

class QueryApp(QWidget):
    """Class for the main query application UI."""
    def __init__(self) -> None:
        """Initialize the query application UI."""
        super().__init__()
        self.db_connector = DbConnect()
        self.current_file = None
        self.init_ui()

    def init_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Data Query Tool")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()

        self.file_button = QPushButton("Select CSV File")
        self.file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.file_button)

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        self.query_grid = QGridLayout()
        self.layout.addLayout(self.query_grid)

        self.setLayout(self.layout)

    def open_file_dialog(self) -> None:
        """Open file dialog to select a CSV file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV",
            os.path.join(os.getcwd(), "tests", "data"),
            "CSV Files (*.csv)"
        )

        if filepath:
            self.file_label.setText(filepath)
            self.current_file = filepath
            self.process_csv(filepath)

    def process_csv(self, filepath: str) -> None:
        """Process the selected CSV file to create a table and query fields.
        Args:
            filepath (str): Path of the selected CSV file.
        """
        table_header = generate_header_from_csv(filepath)
        table_name = get_filename_from_filepath(filepath)
        table_name = table_name.lower()

        if not self.db_connector.is_table_exists(table_name):
            self.db_connector.create_table(table_name, table_header)

            # self.db_connector.add_data_from_data_frame(
            #     table_name,
            #     get_dataframe_from_csv(filepath)
            # )

        self.clear_existing_fields()
        self.add_query_fields(get_dataframe_from_csv(filepath))

    def clear_existing_fields(self) -> None:
        """Clear existing query fields in the UI."""
        for i in reversed(range(self.query_grid.count())):
            widget = self.query_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def add_query_fields(self, data_frame: pd.DataFrame) -> None:
        """Add query fields based on the DataFrame columns.
        Args:
            data_frame (pd.DataFrame): DataFrame containing the data.
        """        
        for i, col in enumerate(data_frame.columns):
            if col == "Make":
                make_options = data_frame["Make"].unique()
                make_combo = QComboBox()
                make_combo.addItems(make_options)
                make_combo.currentTextChanged.connect(self.process_make_fields)
                self.query_grid.addWidget(QLabel("Make"), 0, 0)
                self.query_grid.addWidget(make_combo, 0, 1)

            self.query_grid.addWidget(QLabel(col), i+1, 0)
            query_field = QLineEdit()
            self.query_grid.addWidget(query_field, i+1, 1)

    def process_make_fields(self, selected_make) -> None:
        """Executes a query to retrieve records from the current table where the 'make' field 
        matches the specified value.
        Args:
            selected_make (str): The value to match against the "Make" field in the query.
        Returns:
            None
        """
        current_table = get_filename_from_filepath(self.current_file)
        current_table = current_table.lower()

        query = f'SELECT * FROM {current_table} WHERE "Make" = %s;'

        result = self.db_connector.run_custom_query(query, (selected_make,))
        print(result)
