from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from ...models.tournament import Tournament
from ...models.team import Team
from ...models.match import Match
from .playoff_view import PlayoffBracketWidget

class GroupStandingsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        """Configure table columns and headers."""
        headers = [
            "Position", "Team", "W", "L", "Win%", "+/-"
        ]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for i in range(len(headers)):
            if i != 1:  # All columns except team name
                self.horizontalHeader().setSectionResizeMode(
                    i, QHeaderView.ResizeMode.ResizeToContents
                )
                
    def update_standings(self, standings: list):
        """Update table with current standings."""
        self.setRowCount(len(standings))
        
        for pos, team_stats in enumerate(standings):
            # Position
            pos_item = QTableWidgetItem(str(pos + 1))
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 0, pos_item)
            
            # Team name
            team = team_stats['team']
            team_item = QTableWidgetItem(f"{team.name} ({team.region})")
            self.setItem(pos, 1, team_item)
            
            # Wins
            wins_item = QTableWidgetItem(str(team_stats['wins']))
            wins_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 2, wins_item)
            
            # Losses
            losses_item = QTableWidgetItem(str(team_stats['losses']))
            losses_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 3, losses_item)
            
            # Win percentage
            if team_stats['wins'] + team_stats['losses'] > 0:
                win_pct = team_stats['wins'] / (team_stats['wins'] + team_stats['losses']) * 100
            else:
                win_pct = 0
            win_pct_item = QTableWidgetItem(f"{win_pct:.1f}%")
            win_pct_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 4, win_pct_item)
            
            # Point differential
            diff = team_stats.get('point_diff', 0)
            diff_item = QTableWidgetItem(f"{diff:+d}" if diff != 0 else "0")
            diff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 5, diff_item)

class TournamentView(QWidget):
    def __init__(self, tournament: Tournament, main_window):
        super().__init__()
        self.tournament = tournament
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the tournament view UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        
        title = QLabel(self.tournament.name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        phase_label = QLabel(f"Phase: {self.tournament.current_phase}")
        header_layout.addWidget(phase_label)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        header_layout.addWidget(back_button)
        
        # Tab widget for different views
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Group Stage tab
        group_widget = QWidget()
        group_layout = QVBoxLayout()
        group_widget.setLayout(group_layout)
        
        # Create a tab for each group
        group_tabs = QTabWidget()
        for group_name, teams in self.tournament.groups.items():
            group_tab = QWidget()
            group_tab_layout = QVBoxLayout()
            group_tab.setLayout(group_tab_layout)
            
            # Group standings
            standings_table = GroupStandingsTable()
            standings_table.update_standings(
                self.tournament.group_standings.get(group_name, [])
            )
            group_tab_layout.addWidget(standings_table)
            
            group_tabs.addTab(group_tab, f"Group {group_name}")
            
        group_layout.addWidget(group_tabs)
        tab_widget.addTab(group_widget, "Group Stage")
        
        # Knockout Stage tab
        knockout_widget = QWidget()
        knockout_layout = QVBoxLayout()
        knockout_widget.setLayout(knockout_layout)
        
        # Use PlayoffBracketWidget for knockout stage
        bracket_widget = PlayoffBracketWidget(None)  # TODO: Adapt for tournament
        knockout_layout.addWidget(bracket_widget)
        
        tab_widget.addTab(knockout_widget, "Knockout Stage")
        
        # Statistics tab
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_widget.setLayout(stats_layout)
        
        stats = self.tournament.get_tournament_stats()
        for category, value in stats.items():
            stats_layout.addWidget(QLabel(f"{category}: {value}"))
            
        tab_widget.addTab(stats_widget, "Statistics")
        
    def go_back(self):
        """Return to previous screen."""
        from .main_hub_screen import MainHubScreen
        self.main_window.set_central_widget(
            MainHubScreen(self.main_window)
        )
