import sys

from PySide2.QtWidgets import QApplication

from src.ui_setup import QueryApp

def run_main() -> None:
    """Initialize and run the main application.

    This function creates an instance of the QApplication, sets up the main window,
    and starts the event loop.
    """
    app = QApplication(sys.argv)
    window = QueryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_main()