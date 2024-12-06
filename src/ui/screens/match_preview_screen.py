from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QFrame, QGridLayout, QProgressBar,
                               QGroupBox, QSpacerItem, QSizePolicy, QRadioButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette

from src.models.match import Match
from src.models.team import Team
from src.models.player import Role


class MatchPreviewScreen(QWidget):
    match_started = pyqtSignal(Match)  # Signal emitted when match starts
    draft_started = pyqtSignal(Match, bool)  # Signal emitted when draft starts
    
    def __init__(self, main_window, match: Match):
        super().__init__()
        self.main_window = main_window
        self.match = match
        self.init_ui()
        
    def init_ui(self):
        """Initialize the match preview UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Match header
        header_layout = self.create_header()
        layout.addLayout(header_layout)
        
        # Team comparison section
        team_comparison = self.create_team_comparison()
        layout.addWidget(team_comparison)
        
        # Player matchups section
        player_matchups = self.create_player_matchups()
        layout.addWidget(player_matchups)
        
        # Historical stats section
        historical_stats = self.create_historical_stats()
        layout.addWidget(historical_stats)
        
        # Bottom buttons
        buttons_layout = self.create_buttons()
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
    def create_header(self) -> QHBoxLayout:
        """Create the match header with team names and match info."""
        layout = QHBoxLayout()
        
        # Team 1 name (left)
        team1_name = QLabel(self.match.team1.name)
        team1_name.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        team1_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # VS label (center)
        vs_label = QLabel("VS")
        vs_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vs_label.setStyleSheet("color: #FF4444;")
        
        # Team 2 name (right)
        team2_name = QLabel(self.match.team2.name)
        team2_name.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        team2_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Add to layout with proper spacing
        layout.addWidget(team1_name)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        layout.addWidget(vs_label)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        layout.addWidget(team2_name)
        
        return layout
        
    def create_team_comparison(self) -> QGroupBox:
        """Create the team comparison section."""
        group = QGroupBox("Team Comparison")
        layout = QGridLayout()
        
        metrics = [
            ("Overall Rating", self.calculate_team_rating(self.match.team1), 
             self.calculate_team_rating(self.match.team2)),
            ("Recent Form", self.match.team1.win_rate, self.match.team2.win_rate),
            ("Team Synergy", 75, 80),  # TODO: Implement actual synergy calculation
            ("Experience", 65, 70)      # TODO: Implement experience calculation
        ]
        
        for i, metric in enumerate(metrics):
            label, team1_value, team2_value = metric  # Unpack the tuple
            
            # Add label
            layout.addWidget(QLabel(label), i, 1)
            
            # Add team 1 progress bar
            team1_bar = QProgressBar()
            team1_bar.setMinimum(0)
            team1_bar.setMaximum(100)
            team1_bar.setValue(int(team1_value))
            layout.addWidget(team1_bar, i, 0)
            
            # Add team 2 progress bar
            team2_bar = QProgressBar()
            team2_bar.setMinimum(0)
            team2_bar.setMaximum(100)
            team2_bar.setValue(int(team2_value))
            layout.addWidget(team2_bar, i, 2)
        
        group.setLayout(layout)
        return group
        
    def create_player_matchups(self) -> QGroupBox:
        """Create the player matchups comparison."""
        group = QGroupBox("Player Matchups")
        layout = QGridLayout()
        
        headers = ["Role", "Player", "Rating", "VS", "Rating", "Player"]
        for i, header in enumerate(headers):
            label = QLabel(header)
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            layout.addWidget(label, 0, i)
        
        # Add player matchups for each role
        row = 1
        for role in Role:
            # Get players for this role, with placeholders if missing
            team1_players = self.match.team1.roster.get(role, [])
            team2_players = self.match.team2.roster.get(role, [])
            
            team1_player = team1_players[0] if team1_players else None
            team2_player = team2_players[0] if team2_players else None
            
            # Add role
            layout.addWidget(QLabel(role.value), row, 0)
            
            # Team 1 player
            if team1_player:
                layout.addWidget(QLabel(team1_player.name), row, 1)
                layout.addWidget(QLabel(f"{team1_player.stats.overall_rating:.1f}"), row, 2)
            else:
                layout.addWidget(QLabel("TBD"), row, 1)
                layout.addWidget(QLabel("-"), row, 2)
            
            # VS
            vs_label = QLabel("VS")
            vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(vs_label, row, 3)
            
            # Team 2 player
            if team2_player:
                layout.addWidget(QLabel(f"{team2_player.stats.overall_rating:.1f}"), row, 4)
                layout.addWidget(QLabel(team2_player.name), row, 5)
            else:
                layout.addWidget(QLabel("-"), row, 4)
                layout.addWidget(QLabel("TBD"), row, 5)
            
            row += 1
        
        group.setLayout(layout)
        return group
        
    def create_historical_stats(self) -> QGroupBox:
        """Create the historical stats section."""
        group = QGroupBox("Historical Stats")
        layout = QGridLayout()
        
        # Add head-to-head record
        h2h_label = QLabel("Head-to-Head Record:")
        layout.addWidget(h2h_label, 0, 0)
        
        # TODO: Implement actual head-to-head record tracking
        h2h_record = QLabel("0-0")
        layout.addWidget(h2h_record, 0, 1)
        
        # Add last 5 matches
        last_matches_label = QLabel("Last 5 Matches:")
        layout.addWidget(last_matches_label, 1, 0)
        
        # TODO: Implement actual match history
        team1_record = QLabel(f"{self.match.team1.name}: W-W-L-W-L")
        team2_record = QLabel(f"{self.match.team2.name}: L-W-W-L-W")
        layout.addWidget(team1_record, 1, 1)
        layout.addWidget(team2_record, 2, 1)
        
        group.setLayout(layout)
        return group
        
    def create_buttons(self) -> QHBoxLayout:
        """Create the bottom buttons."""
        layout = QHBoxLayout()
        
        # Add spacer
        layout.addStretch()
        
        # Start Match button
        start_btn = QPushButton("Start Match")
        start_btn.clicked.connect(self.start_match)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(start_btn)
        
        return layout
        
    def start_match(self):
        """Start the draft phase before the match."""
        # team1 is always the home team in the match, so it should be blue side
        team1_is_blue = True
        self.draft_started.emit(self.match, team1_is_blue)
    
    def calculate_team_rating(self, team: Team) -> float:
        """Calculate overall team rating."""
        if not team.roster:
            return 0.0
            
        total_rating = 0
        num_players = 0
        
        for role in Role:
            players = team.roster[role]
            if players:
                total_rating += players[0].stats.overall_rating  # Use starting player's rating
                num_players += 1
        
        return total_rating / num_players if num_players > 0 else 0.0
