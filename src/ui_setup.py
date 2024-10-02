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

from .db_connect import DbConnect

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
