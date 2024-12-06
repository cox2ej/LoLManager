import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
