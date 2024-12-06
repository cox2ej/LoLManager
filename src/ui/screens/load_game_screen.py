from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoadGameScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the load game screen UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Add title
        title = QLabel("Load Game")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(title)
        
        # Create save game list
        self.save_list = QListWidget()
        self.save_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                border: 1px solid #666666;
            }
            QListWidget::item:hover {
                background-color: #333333;
                border: 1px solid #666666;
            }
        """)
        
        # Add sample save games (TODO: Replace with actual save files)
        sample_saves = [
            "Save 1 - Team NA - Season 1 - 2024-03-20",
            "Save 2 - Team EU - Season 2 - 2024-03-19",
            "Save 3 - Team KR - Season 1 - 2024-03-18"
        ]
        
        for save in sample_saves:
            item = QListWidgetItem(save)
            self.save_list.addItem(item)
        
        layout.addWidget(self.save_list)
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        # Create buttons
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_game)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_save)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_title_screen)
        
        # Style buttons
        for button in [load_button, delete_button, back_button]:
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
        button_layout.addWidget(delete_button)
        button_layout.addWidget(load_button)
        
        layout.addLayout(button_layout)
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
        """)
        
        self.setLayout(layout)
    
    def load_game(self):
        """Load the selected save game."""
        current_item = self.save_list.currentItem()
        if current_item:
            save_name = current_item.text()
            # TODO: Implement actual save game loading
            print(f"Loading save game: {save_name}")
        else:
            # TODO: Show error message
            print("No save game selected")
    
    def delete_save(self):
        """Delete the selected save game."""
        current_item = self.save_list.currentItem()
        if current_item:
            save_name = current_item.text()
            # TODO: Implement actual save game deletion
            print(f"Deleting save game: {save_name}")
            self.save_list.takeItem(self.save_list.row(current_item))
        else:
            # TODO: Show error message
            print("No save game selected")
