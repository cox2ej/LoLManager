from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QCheckBox, QSpinBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SettingsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the settings screen UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Add title
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(title)
        
        # Create form layout for settings
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Sound settings
        self.sound_enabled = QCheckBox()
        self.sound_enabled.setChecked(True)
        form_layout.addRow("Sound Effects:", self.sound_enabled)
        
        # Music settings
        self.music_enabled = QCheckBox()
        self.music_enabled.setChecked(True)
        form_layout.addRow("Background Music:", self.music_enabled)
        
        # Volume control
        self.volume = QSpinBox()
        self.volume.setRange(0, 100)
        self.volume.setValue(50)
        self.volume.setStyleSheet("""
            QSpinBox {
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QSpinBox:hover {
                border: 2px solid #666666;
            }
        """)
        form_layout.addRow("Volume:", self.volume)
        
        # Auto-save settings
        self.auto_save = QCheckBox()
        self.auto_save.setChecked(True)
        form_layout.addRow("Auto-save:", self.auto_save)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        # Create buttons
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_title_screen)
        
        # Style buttons
        for button in [save_button, back_button]:
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
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
            QCheckBox {
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #2a2a2a;
                border: 2px solid #333333;
                border-radius: 5px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #333333;
                border-radius: 5px;
            }
        """)
        
        self.setLayout(layout)
    
    def save_settings(self):
        """Save the current settings."""
        settings = {
            'sound_enabled': self.sound_enabled.isChecked(),
            'music_enabled': self.music_enabled.isChecked(),
            'volume': self.volume.value(),
            'auto_save': self.auto_save.isChecked()
        }
        
        # TODO: Save settings to configuration file
        print("Saving settings:", settings)
        self.main_window.show_title_screen()
