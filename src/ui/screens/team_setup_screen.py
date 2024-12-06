from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QScrollArea, QFrame,
                           QGridLayout, QSpinBox, QMessageBox, QTableWidget,
                           QTableWidgetItem, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QColor
from src.models.team import Team
from src.models.player import Player, PlayerStats, Role
from src.models.league import League, Split
from src.data.teams import create_default_teams
from datetime import date, timedelta, datetime

class TeamSetupScreen(QWidget):
    def __init__(self, main_window, selected_region):
        super().__init__()
        self.main_window = main_window
        self.selected_region = selected_region
        self.selected_team = None
        self.teams = create_default_teams()
        self.filtered_teams = self.filter_teams_by_region()
        self.init_ui()
    
    def filter_teams_by_region(self):
        """Filter teams by selected region."""
        region_mapping = {
            "Korea": "KR",
            "Europe": "EU",
            "China": "CN",
            "North America": "NA"
        }
        return {name: team for name, team in self.teams.items() 
                if team.region == region_mapping.get(self.selected_region, self.selected_region)}
    
    def init_ui(self):
        """Initialize the team setup UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Team Selection")
        header_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Team selection
        team_selection = self.create_team_selection()
        layout.addWidget(team_selection)
        
        # Team info
        self.team_info_widget = self.create_team_info()
        layout.addWidget(self.team_info_widget)
        
        # Roster display
        self.roster_widget = self.create_roster_display()
        layout.addWidget(self.roster_widget)
        
        # Confirm button
        confirm_btn = QPushButton("Confirm Selection")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        confirm_btn.clicked.connect(self.confirm_selection)
        layout.addWidget(confirm_btn)
        
        self.setLayout(layout)
        
    def create_team_selection(self):
        """Create the team selection dropdown."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        label = QLabel("Select Your Team:")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)
        
        self.team_combo = QComboBox()
        self.team_combo.addItems(sorted(self.filtered_teams.keys()))
        self.team_combo.currentTextChanged.connect(self.on_team_selected)
        layout.addWidget(self.team_combo)
        
        frame.setLayout(layout)
        return frame
    
    def create_team_info(self):
        """Create the team information display."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QGridLayout()
        
        # Create labels but don't populate them yet
        self.team_info_labels = {
            'Championships': QLabel(),
            'Budget': QLabel(),
            'Fanbase': QLabel(),
            'Training Facilities': QLabel(),
            'Brand Value': QLabel()
        }
        
        row = 0
        for key, label in self.team_info_labels.items():
            layout.addWidget(QLabel(f"{key}:"), row, 0)
            layout.addWidget(label, row, 1)
            row += 1
            
        frame.setLayout(layout)
        return frame
    
    def create_roster_display(self):
        """Create the roster display table."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Team Roster")
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Create table
        self.roster_table = QTableWidget()
        self.roster_table.setColumnCount(6)
        self.roster_table.setHorizontalHeaderLabels([
            "Role", "Name", "Nationality", "Overall Rating", "Salary", "Contract End"
        ])
        
        # Set table properties
        self.roster_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.roster_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.roster_table)
        frame.setLayout(layout)
        return frame
    
    def on_team_selected(self, team_name):
        """Handle team selection."""
        if not team_name:
            return
            
        self.selected_team = self.teams[team_name]
        
        # Update team info
        self.team_info_labels['Championships'].setText(str(self.selected_team.championships))
        self.team_info_labels['Budget'].setText(f"${self.selected_team.budget:,}")
        self.team_info_labels['Fanbase'].setText(f"{self.selected_team.fanbase:,}")
        self.team_info_labels['Training Facilities'].setText(str(self.selected_team.training_facilities))
        self.team_info_labels['Brand Value'].setText(str(self.selected_team.brand_value))
        
        # Update roster display
        self.update_roster_display()
    
    def update_roster_display(self):
        """Update the roster table with current team's players."""
        if not self.selected_team:
            return
            
        # Clear existing rows
        self.roster_table.setRowCount(0)
        
        # Add players to table
        for role in Role:
            players = self.selected_team.roster[role]
            if players:
                player = players[0]  # Get the first (starting) player
                row = self.roster_table.rowCount()
                self.roster_table.insertRow(row)
                
                # Add player info
                self.roster_table.setItem(row, 0, QTableWidgetItem(role.value))
                self.roster_table.setItem(row, 1, QTableWidgetItem(player.name))
                self.roster_table.setItem(row, 2, QTableWidgetItem(player.nationality))
                self.roster_table.setItem(row, 3, QTableWidgetItem(f"{player.stats.overall_rating:.1f}"))
                self.roster_table.setItem(row, 4, QTableWidgetItem(f"${player.salary:,}"))
                self.roster_table.setItem(row, 5, QTableWidgetItem(player.contract_end.strftime('%Y-%m-%d')))
    
    def confirm_selection(self):
        """Confirm team selection and proceed."""
        if not self.selected_team:
            QMessageBox.warning(self, "Warning", "Please select a team first!")
            return
            
        # Create the appropriate league based on region
        if self.selected_region == "Korea":
            from src.data.lck_teams import create_lck_league
            league = create_lck_league()
        elif self.selected_region == "Europe":
            from src.data.lec_teams import create_lec_league
            league = create_lec_league()
        elif self.selected_region == "China":
            from src.data.lpl_teams import create_lpl_league
            league = create_lpl_league()
        elif self.selected_region == "North America":
            from src.data.lcs_teams import create_lcs_league
            league = create_lcs_league()
        else:
            QMessageBox.warning(self, "Error", f"Invalid region: {self.selected_region}")
            return

        # Set the player's team in the main window
        self.main_window.player_team = self.selected_team
        
        # Initialize the league and show the main hub
        self.main_window.start_league(league)