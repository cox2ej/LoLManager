from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QLabel,
    QPushButton, QComboBox, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from typing import Dict, List, Optional

from ...models.league import League, Division, SeasonPhase
from ...models.team import Team
from ...models.match import Match, MatchResult


class StandingsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
    
    def setup_table(self):
        """Configure table columns and headers."""
        headers = [
            "Position", "Team", "W", "L", "Win%", 
            "Streak", "+/-", "Points", "Last 5"
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

    def update_standings(self, standings: List[Dict]):
        """Update table with current standings."""
        self.setRowCount(len(standings))
        
        for pos, team_stats in enumerate(standings):
            team = team_stats['team']
            
            # Position
            pos_item = QTableWidgetItem(str(pos + 1))
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 0, pos_item)
            
            # Team name
            team_item = QTableWidgetItem(team.name)
            self.setItem(pos, 1, team_item)
            
            # Wins
            wins_item = QTableWidgetItem(str(team_stats['wins']))
            wins_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 2, wins_item)
            
            # Losses
            losses_item = QTableWidgetItem(str(team_stats['losses']))
            losses_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 3, losses_item)
            
            # Win Rate
            winrate = f"{team_stats['win_rate']:.1f}%"
            winrate_item = QTableWidgetItem(winrate)
            winrate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 4, winrate_item)
            
            # Streak
            streak = team_stats['streak']
            streak_text = f"W{streak}" if streak > 0 else f"L{abs(streak)}"
            streak_item = QTableWidgetItem(streak_text)
            streak_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 5, streak_item)
            
            # Game Differential
            diff = team_stats['game_diff']
            diff_text = f"+{diff}" if diff > 0 else str(diff)
            diff_item = QTableWidgetItem(diff_text)
            diff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 6, diff_item)
            
            # Championship Points
            points_item = QTableWidgetItem(str(team_stats['points']))
            points_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 7, points_item)
            
            # Last 5 matches (placeholder for now)
            last5_item = QTableWidgetItem("---")
            last5_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(pos, 8, last5_item)


class ScheduleTable(QTableWidget):
    match_selected = pyqtSignal(Match)
    
    def __init__(self):
        super().__init__()
        self.setup_table()
    
    def setup_table(self):
        """Configure table columns and headers."""
        headers = ["Week", "Day", "Home", "Away", "Score", "Status"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        for i in [0, 1, 4, 5]:
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents
            )
    
    def update_schedule(self, matches: List[Match], current_week: int):
        """Update table with match schedule."""
        # Sort matches by date
        sorted_matches = sorted(matches, key=lambda m: m.match_date)
        self.setRowCount(len(sorted_matches))
        
        current_week = None
        current_date = None
        row_index = 0
        
        for match in sorted_matches:
            # Calculate week number (1-based)
            week_num = (match.match_date - sorted_matches[0].match_date).days // 7 + 1
            date_str = match.match_date.strftime("%a %Y-%m-%d")
            
            # Add week header if new week
            if week_num != current_week:
                current_week = week_num
                current_date = None
                if row_index > 0:
                    self.insertRow(row_index)
                    self.set_empty_row(row_index)
                    row_index += 1
            
            # Add date header if new date
            if date_str != current_date:
                current_date = date_str
                self.insertRow(row_index)
                date_item = QTableWidgetItem(date_str)
                date_item.setBackground(QColor("#2a2a2a"))
                self.setItem(row_index, 1, date_item)
                self.set_empty_row(row_index, skip_date=True)
                row_index += 1
            
            # Week
            week_item = QTableWidgetItem(str(week_num))
            week_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row_index, 0, week_item)
            
            # Home Team
            home_item = QTableWidgetItem(match.team1.name)
            self.setItem(row_index, 2, home_item)
            
            # Away Team
            away_item = QTableWidgetItem(match.team2.name)
            self.setItem(row_index, 3, away_item)
            
            # Score
            score_text = "-"
            if match.result:
                score_text = f"{match.result.winner_score}-{match.result.loser_score}"
            score_item = QTableWidgetItem(score_text)
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row_index, 4, score_item)
            
            # Status
            status = "Upcoming"
            if match.result:
                status = "Completed"
            elif week_num == current_week:
                status = "Next"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row_index, 5, status_item)
            
            row_index += 1
    
    def set_empty_row(self, row: int, skip_date: bool = False):
        """Set empty items for a row to maintain consistent styling."""
        for col in range(self.columnCount()):
            if skip_date and col == 1:
                continue
            item = QTableWidgetItem("")
            item.setBackground(QColor("#2a2a2a"))
            self.setItem(row, col, item)


class LeagueView(QWidget):
    def __init__(self, league: League, main_window):
        super().__init__()
        self.league = league
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main league view UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        
        title = QLabel(self.league.name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add playoff button if in playoff phase
        if self.league.current_season and self.league.current_season.phase == SeasonPhase.PLAYOFFS:
            playoff_button = QPushButton("View Playoffs")
            playoff_button.clicked.connect(self.view_playoffs)
            header_layout.addWidget(playoff_button)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        header_layout.addWidget(back_button)
        
        # League Info Header
        header_layout = QHBoxLayout()
        
        # League Selector
        self.league_combo = QComboBox()
        self.league_combo.addItem(self.league.name)  # Add player's league
        # Add other leagues from game state
        for league_name in self.main_window.game_state.other_leagues.keys():
            self.league_combo.addItem(league_name)
        self.league_combo.currentTextChanged.connect(self.on_league_changed)
        header_layout.addWidget(QLabel("League:"))
        header_layout.addWidget(self.league_combo)
        
        league_name = QLabel(f"<h1>{self.league.name}</h1>")
        self.league_title = league_name  # Store reference to update later
        header_layout.addWidget(league_name)
        
        # Season Info
        if self.league.current_season:
            season_info = QLabel(
                f"{self.league.current_season.split.value} Split {self.league.current_season.year} - "
                f"Week {self.league.current_season.current_week + 1}"
            )
            self.season_info = season_info  # Store reference to update later
            header_layout.addWidget(season_info)
        
        header_layout.addStretch()
        
        # Division Selector
        self.division_combo = QComboBox()
        self.division_combo.addItems(self.league.divisions.keys())
        self.division_combo.currentTextChanged.connect(self.on_division_changed)
        header_layout.addWidget(QLabel("Division:"))
        header_layout.addWidget(self.division_combo)
        
        # Simulate Week button
        simulate_btn = QPushButton("Simulate Next Week")
        simulate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        simulate_btn.clicked.connect(self.on_simulate_week)
        header_layout.addWidget(simulate_btn)
        
        layout.addLayout(header_layout)
        
        # Tabs for different views
        tabs = QTabWidget()
        
        # Standings Tab
        standings_widget = QWidget()
        standings_layout = QVBoxLayout()
        self.standings_table = StandingsTable()
        standings_layout.addWidget(self.standings_table)
        standings_widget.setLayout(standings_layout)
        tabs.addTab(standings_widget, "Standings")
        
        # Schedule Tab
        schedule_widget = QWidget()
        schedule_layout = QVBoxLayout()
        self.schedule_table = ScheduleTable()
        schedule_layout.addWidget(self.schedule_table)
        schedule_widget.setLayout(schedule_layout)
        tabs.addTab(schedule_widget, "Schedule")
        
        layout.addWidget(tabs)
        
        # Control Buttons
        button_layout = QHBoxLayout()
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Initial update
        self.update_view()
    
    def update_view(self):
        """Update all views with current data."""
        current_division = self.division_combo.currentText()
        if current_division in self.league.divisions:
            division = self.league.divisions[current_division]
            
            # Update standings
            standings = division.get_standings()
            self.standings_table.update_standings(standings)
            
            # Update schedule
            if self.league.current_season:
                self.schedule_table.update_schedule(
                    division.matches,
                    self.league.current_season.current_week
                )
    
    def on_division_changed(self, division_name: str):
        """Handle division selection change."""
        self.update_view()
    
    def on_league_changed(self, league_name: str):
        """Handle league selection change."""
        if league_name == self.main_window.game_state.league.name:
            current_league = self.main_window.game_state.league
        else:
            current_league = self.main_window.game_state.other_leagues[league_name]
        
        # Update UI elements
        self.league = current_league
        self.league_title.setText(f"<h1>{current_league.name}</h1>")
        
        # Update season info if available
        if current_league.current_season and hasattr(self, 'season_info'):
            self.season_info.setText(
                f"{current_league.current_season.split.value} Split {current_league.current_season.year} - "
                f"Week {current_league.current_season.current_week + 1}"
            )
        
        # Update division selector
        self.division_combo.clear()
        self.division_combo.addItems(current_league.divisions.keys())
        
        # Update view with new league data
        self.update_view()

    def on_simulate_week(self):
        """Simulate all matches for the current week."""
        try:
            # Get game state from main window
            game_state = self.main_window.game_state
            if not game_state:
                raise ValueError("Game state not initialized")
            
            # Get player's team
            player_team = game_state.current_team
            if not player_team:
                raise ValueError("Player team not initialized")
            
            # Simulate all leagues
            all_results = game_state.simulate_all_leagues()
            self.update_view()
            
            # Show results in a message box
            result_text = "Match Results:\n\n"
            for league_name, league_results in all_results.items():
                result_text += f"{league_name}:\n"
                for division_name, division_results in league_results.items():
                    if division_results:  # Only show divisions with results
                        result_text += f"{division_name} Division:\n"
                        for result in division_results:
                            result_text += f"{result.winner.name} def. {result.loser.name} ({result.winner_score}-{result.loser_score})\n"
                        result_text += "\n"
                result_text += "\n"
            
            if not any(any(results.values()) for results in all_results.values()):
                result_text = "No matches to simulate this week."
            
            QMessageBox.information(self, "Week Simulated", result_text)
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def view_playoffs(self):
        """Switch to playoff view."""
        from .playoff_view import PlayoffView
        self.main_window.set_central_widget(
            PlayoffView(self.league, self.main_window)
        )
    
    def go_back(self):
        """Handle back button click."""
        self.main_window.show_main_hub_screen()
