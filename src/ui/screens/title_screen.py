from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                               QLabel, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class TitleScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the title screen UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Add title
        title = QLabel("League of Legends Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(title)
        
        # Add subtitle
        subtitle = QLabel("Build Your Dynasty")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont("Arial", 18)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(subtitle)
        
        # Add spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))
        
        # Create buttons
        buttons = [
            ("New Game", self.main_window.show_new_game_screen),
            ("Load Game", self.main_window.show_load_game_screen),
            ("Settings", self.main_window.show_settings_screen),
            ("Exit", self.main_window.close)
        ]
        
        # Add buttons
        for text, callback in buttons:
            button = QPushButton(text)
            button.setMinimumSize(200, 50)
            button.clicked.connect(callback)
            button.setFont(QFont("Arial", 12))
            # Style the button
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
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add bottom spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
        """)
        
        self.setLayout(layout)
    
    def new_game(self):
        """Start a new game."""
        # TODO: Implement new game functionality
        print("Starting new game...")
    
    def load_game(self):
        """Load an existing game."""
        # TODO: Implement load game functionality
        print("Loading game...")
    
    def show_settings(self):
        """Show settings screen."""
        # TODO: Implement settings screen
        print("Opening settings...")
