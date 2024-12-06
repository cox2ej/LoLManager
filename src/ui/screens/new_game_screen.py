from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QComboBox, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class NewGameScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the new game screen UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Add title
        title = QLabel("Create New Game")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(title)
        
        # Create form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Manager name input
        self.manager_name = QLineEdit()
        self.manager_name.setMinimumWidth(200)
        self.manager_name.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #666666;
            }
        """)
        form_layout.addRow("Manager Name:", self.manager_name)
        
        # Region selection
        self.region = QComboBox()
        self.region.addItems(["Korea", "Europe", "China", "North America"])
        self.region.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                border: 2px solid #666666;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-width: 0px;
            }
        """)
        form_layout.addRow("Starting Region:", self.region)
        
        # Difficulty selection
        self.difficulty = QComboBox()
        self.difficulty.addItems(["Easy", "Normal", "Hard"])
        self.difficulty.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                border: 2px solid #666666;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-width: 0px;
            }
        """)
        form_layout.addRow("Difficulty:", self.difficulty)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        # Create buttons
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_title_screen)
        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.start_game)
        
        # Style buttons
        for button in [back_button, continue_button]:
            button.setMinimumSize(150, 40)
            button.setFont(QFont("Arial", 12))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #1a1a1a;
                    color: white;
                    border: 2px solid #333333;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #333333;
                    border: 2px solid #666666;
                }
                QPushButton:pressed {
                    background-color: #666666;
                }
            """)
        
        # Add buttons to layout
        button_layout.addWidget(back_button)
        button_layout.addWidget(continue_button)
        
        layout.addLayout(button_layout)
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
        """)
        
        self.setLayout(layout)
    
    def start_game(self):
        """Start a new game with the entered information."""
        manager_name = self.manager_name.text().strip()
        selected_region = self.region.currentText()
        
        if not manager_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a manager name.")
            return
        
        # Show team setup screen with selected region
        self.main_window.show_team_setup_screen(selected_region)
