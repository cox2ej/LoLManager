from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QFrame, QGridLayout, QScrollArea, QTableWidget,
                               QTableWidgetItem, QProgressBar, QTabWidget, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from src.game.game_state import GameState
from src.database.db_manager import DatabaseManager
from src.models.player import Player, PlayerStats, Role
from src.models.match import Match
from src.models.team import Team
from src.ui.screens.league_view import LeagueView, ScheduleTable

class MainHubScreen(QWidget):
    def __init__(self, main_window, game_state: GameState = None):
        super().__init__()
        self.main_window = main_window
        self.game_state = game_state
        self.init_ui()
        # Call update_ui after initialization
        self.update_ui()

    def showEvent(self, event):
        """Called when the screen becomes visible."""
        super().showEvent(event)
        # Update UI whenever screen is shown
        self.update_ui()

    def update_ui(self):
        """Update all UI elements with current game state."""
        if not self.game_state or not self.game_state.current_team:
            print("No game state or team available")
            return

        team = self.game_state.current_team
        print(f"Updating UI with team: {team.name}")

        # Update header
        self.team_name_label.setText(team.name)
        self.team_region_label.setText(f"Region: {team.region}")

        # Update key stats
        stats = [
            ("League Position", self.game_state.get_league_position()),
            ("Season", self.game_state.season),
            ("Win Rate", f"{self.game_state.get_win_rate():.1f}%"),
            ("Budget", f"${team.budget:,}")
        ]

        for i, (label, value) in enumerate(stats):
            self.stats_grid.itemAtPosition(i, 1).widget().setText(value)

        # Update performance metrics
        self.update_performance_metrics()

        # Update recent results
        results = self.game_state.get_recent_results()
        
        # Clear existing items first
        for row in range(self.results_table.rowCount()):
            for col in range(self.results_table.columnCount()):
                self.results_table.setItem(row, col, QTableWidgetItem(""))
        
        # Add new results
        for i, result in enumerate(results):
            if i < self.results_table.rowCount():  # Make sure we don't exceed table rows
                self.results_table.setItem(i, 0, QTableWidgetItem(result["date"]))
                self.results_table.setItem(i, 1, QTableWidgetItem(result["opponent"]))
                self.results_table.setItem(i, 2, QTableWidgetItem(result["score"]))
                result_item = QTableWidgetItem(result["result"])
                result_item.setForeground(QColor("#4CAF50" if result["result"] == "WIN" else "#F44336"))
                self.results_table.setItem(i, 3, result_item)

        # Update roster
        self.update_roster_table()

        # Update schedule
        if (hasattr(self.game_state, 'league') and 
            self.game_state.league and 
            self.game_state.league.current_season and
            self.game_state.current_team):
            
            league = self.game_state.league
            current_week = league.current_season.current_week
            current_team = self.game_state.current_team
            
            # Get all matches from all divisions
            team_matches = []
            
            # First get all matches from the league
            for division in league.divisions.values():
                if division and division.matches:
                    # Filter matches involving the player's team
                    division_matches = [
                        match for match in division.matches 
                        if match.team1 == current_team or match.team2 == current_team
                    ]
                    team_matches.extend(division_matches)
            
            # Sort matches by date
            if team_matches:
                team_matches.sort(key=lambda m: m.match_date)
                self.schedule_table.update_schedule(team_matches, current_week)
                print(f"Found {len(team_matches)} matches for team {current_team.name}")  # Debug print
            else:
                print(f"No matches found for team: {current_team.name}")  # Debug print
                print(f"League: {league.name}, Season: {league.current_season.split}")
                print(f"Divisions: {[d.name for d in league.divisions.values()]}")
                for div in league.divisions.values():
                    print(f"Division {div.name} has {len(div.matches)} matches")

        # Update finances
        finances = self.game_state.get_financial_overview()
        for i, (label, value) in enumerate(finances.items()):
            self.finance_grid.itemAtPosition(i, 1).widget().setText(value)

        # Update facilities
        facilities = self.game_state.get_facility_levels()
        for facility, level in facilities.items():
            self.facility_bars[facility].setValue(level)

    def update_performance_metrics(self):
        """Update the performance metrics display."""
        if not self.game_state or not self.game_state.current_team:
            return
            
        performance = self.game_state.get_team_performance()
        print(f"Team performance metrics: {performance}")  # Debug print
        
        # Update progress bars
        self.synergy_bar.setValue(int(performance["synergy"]))
        self.morale_bar.setValue(int(performance["morale"]))
        self.form_bar.setValue(int(performance["form"]))
        self.overall_bar.setValue(int(performance["overall"]))
        
        # Update labels
        self.synergy_label.setText(f"Team Synergy: {performance['synergy']}%")
        self.morale_label.setText(f"Team Morale: {performance['morale']}%")
        self.form_label.setText(f"Current Form: {performance['form']}%")
        self.overall_label.setText(f"Overall Performance: {performance['overall']}%")

    def update_roster_table(self):
        """Update the roster table with current team data."""
        if not self.game_state or not self.game_state.current_team:
            print("No game state or team available")  # Debug print
            return
            
        team = self.game_state.current_team
        print(f"Updating roster table for team {team.name}")  # Debug print
        print(f"Roster: {team.roster}")  # Debug print
        
        # Clear existing rows
        self.roster_table.setRowCount(0)
        
        # Add players to table
        row = 0
        for role in Role:  # Use Role enum
            players = team.roster[role]  # Access roster with Role enum
            print(f"Role {role.name}: {len(players)} players")  # Debug print
            
            for player in players:
                print(f"Adding player {player.name} to row {row}")  # Debug print
                self.roster_table.insertRow(row)
                
                # Add player data to table
                self.roster_table.setItem(row, 0, QTableWidgetItem(player.name))
                self.roster_table.setItem(row, 1, QTableWidgetItem(role.value))  # Use role.value for display
                self.roster_table.setItem(row, 2, QTableWidgetItem(str(player.stats.mechanical_skill)))
                self.roster_table.setItem(row, 3, QTableWidgetItem(str(player.stats.game_knowledge)))
                self.roster_table.setItem(row, 4, QTableWidgetItem(str(player.stats.communication)))
                self.roster_table.setItem(row, 5, QTableWidgetItem(str(player.stats.leadership)))
                self.roster_table.setItem(row, 6, QTableWidgetItem(f"${player.salary:,}"))
                self.roster_table.setItem(row, 7, QTableWidgetItem(player.contract_end.strftime("%Y-%m-%d")))
                
                row += 1
        
        # Auto-adjust row heights
        self.roster_table.resizeRowsToContents()

    def init_ui(self):
        """Initialize the main hub screen UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Add header with team info
        header_layout = self.create_header()
        layout.addLayout(header_layout)

        # Create main content area with tabs
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #1a1a1a;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #2a2a2a;
                color: white;
                padding: 8px 20px;
                border: 1px solid #333333;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #1a1a1a;
                border-bottom: none;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)

        # Add tabs
        tab_widget.addTab(self.create_overview_tab(), "Overview")
        tab_widget.addTab(self.create_roster_tab(), "Roster")
        tab_widget.addTab(self.create_schedule_tab(), "Schedule")
        tab_widget.addTab(self.create_finances_tab(), "Finances")
        tab_widget.addTab(self.create_facilities_tab(), "Facilities")

        layout.addWidget(tab_widget)

        # Add quick actions bar at bottom
        actions_layout = self.create_quick_actions()
        layout.addLayout(actions_layout)

        self.setLayout(layout)

    def create_header(self):
        """Create the header section with team info."""
        header_layout = QHBoxLayout()

        # Team name and logo (left)
        team_info = QFrame()
        team_info.setStyleSheet("background-color: #2a2a2a; border-radius: 10px; padding: 10px;")
        team_layout = QVBoxLayout()

        self.team_name_label = QLabel("Team Name")
        self.team_name_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        team_layout.addWidget(self.team_name_label)

        self.team_region_label = QLabel("Region: NA")
        team_layout.addWidget(self.team_region_label)

        team_info.setLayout(team_layout)
        header_layout.addWidget(team_info, stretch=2)

        # Key stats (right)
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #2a2a2a; border-radius: 10px; padding: 10px;")
        stats_layout = QGridLayout()

        stats = [
            ("League Position", "1st"),
            ("Season", "Spring 2024"),
            ("Win Rate", "75%"),
            ("Budget", "$5,000,000"),
        ]

        for i, (label, value) in enumerate(stats):
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Arial", 10))
            value_widget = QLabel(value)
            value_widget.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            stats_layout.addWidget(label_widget, i, 0)
            stats_layout.addWidget(value_widget, i, 1)

        self.stats_grid = stats_layout

        stats_frame.setLayout(stats_layout)
        header_layout.addWidget(stats_frame, stretch=1)

        return header_layout

    def create_overview_tab(self):
        """Create the overview tab with team performance metrics."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Create performance metrics section
        metrics_group = QGroupBox("Team Performance")
        metrics_layout = QGridLayout()
        
        # Create progress bars and labels for each metric
        self.synergy_bar = QProgressBar()
        self.morale_bar = QProgressBar()
        self.form_bar = QProgressBar()
        self.overall_bar = QProgressBar()
        
        self.synergy_label = QLabel("Team Synergy: 0%")
        self.morale_label = QLabel("Team Morale: 0%")
        self.form_label = QLabel("Current Form: 0%")
        self.overall_label = QLabel("Overall Performance: 0%")
        
        # Style progress bars
        for bar in [self.synergy_bar, self.morale_bar, self.form_bar, self.overall_bar]:
            bar.setMinimum(0)
            bar.setMaximum(100)
            bar.setTextVisible(True)
            bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    width: 10px;
                    margin: 0.5px;
                }
            """)
        
        # Add metrics to layout
        metrics_layout.addWidget(self.synergy_label, 0, 0)
        metrics_layout.addWidget(self.synergy_bar, 0, 1)
        metrics_layout.addWidget(self.morale_label, 1, 0)
        metrics_layout.addWidget(self.morale_bar, 1, 1)
        metrics_layout.addWidget(self.form_label, 2, 0)
        metrics_layout.addWidget(self.form_bar, 2, 1)
        metrics_layout.addWidget(self.overall_label, 3, 0)
        metrics_layout.addWidget(self.overall_bar, 3, 1)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Add recent results section
        results_group = QGroupBox("Recent Results")
        results_layout = QVBoxLayout()
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setRowCount(5)  # Set fixed number of rows for recent results
        self.results_table.setHorizontalHeaderLabels(["Date", "Opponent", "Score", "Result"])
        
        # Style the table
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #1a1a1a;
                gridline-color: #333333;
                border: none;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                padding: 5px;
                border: 1px solid #333333;
                color: white;
            }
            QTableWidget::item {
                padding: 5px;
                color: white;
            }
        """)
        
        # Set column widths
        self.results_table.setColumnWidth(0, 100)  # Date
        self.results_table.setColumnWidth(1, 150)  # Opponent
        self.results_table.setColumnWidth(2, 80)   # Score
        self.results_table.setColumnWidth(3, 80)   # Result
        
        results_layout.addWidget(self.results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        tab.setLayout(layout)
        return tab

    def create_roster_tab(self):
        """Create the roster tab with player information."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Create roster table
        self.roster_table = QTableWidget()
        self.roster_table.setColumnCount(8)
        self.roster_table.setHorizontalHeaderLabels([
            "Name", "Role", "Mechanical", "Game Knowledge", 
            "Communication", "Leadership", "Salary", "Contract End"
        ])
        
        # Style the table
        self.roster_table.setStyleSheet("""
            QTableWidget {
                background-color: #1a1a1a;
                gridline-color: #333333;
                border: none;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                padding: 5px;
                border: 1px solid #333333;
                color: white;
            }
            QTableWidget::item {
                padding: 5px;
                color: white;
            }
        """)
        
        # Set column widths
        self.roster_table.setColumnWidth(0, 150)  # Name
        self.roster_table.setColumnWidth(1, 100)  # Role
        self.roster_table.setColumnWidth(2, 100)  # Mechanical
        self.roster_table.setColumnWidth(3, 120)  # Game Knowledge
        self.roster_table.setColumnWidth(4, 120)  # Communication
        self.roster_table.setColumnWidth(5, 100)  # Leadership
        self.roster_table.setColumnWidth(6, 100)  # Salary
        self.roster_table.setColumnWidth(7, 120)  # Contract End
        
        layout.addWidget(self.roster_table)
        tab.setLayout(layout)
        return tab

    def create_schedule_tab(self):
        """Create the schedule and calendar tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Add view full schedule button
        view_schedule_btn = QPushButton("View Full League Schedule")
        view_schedule_btn.clicked.connect(self.show_league_view)
        layout.addWidget(view_schedule_btn)
        
        # Add schedule table
        self.schedule_table = ScheduleTable()
        layout.addWidget(self.schedule_table)
        
        tab.setLayout(layout)
        return tab

    def create_finances_tab(self):
        """Create the financial management tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        # Financial Overview
        finance_frame = QFrame()
        finance_frame.setStyleSheet("background-color: #2a2a2a; border-radius: 10px; padding: 15px;")
        finance_layout = QVBoxLayout()

        finance_title = QLabel("Financial Overview")
        finance_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        finance_layout.addWidget(finance_title)

        # Financial metrics
        metrics = [
            ("Current Budget", "$5,000,000"),
            ("Weekly Salary Expenses", "$23,400"),
            ("Sponsorship Income", "$100,000/month"),
            ("Merchandise Revenue", "$50,000/month"),
            ("Facility Maintenance", "$10,000/month")
        ]

        self.finance_grid = QGridLayout()
        for i, (label, value) in enumerate(metrics):
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Arial", 12))
            value_widget = QLabel(value)
            value_widget.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.finance_grid.addWidget(label_widget, i, 0)
            self.finance_grid.addWidget(value_widget, i, 1)

        finance_layout.addLayout(self.finance_grid)
        finance_frame.setLayout(finance_layout)
        layout.addWidget(finance_frame)

        # Financial Actions
        buttons_layout = QHBoxLayout()

        actions = ["Manage Budget", "Sponsorship Deals", "View Financial Report", "Revenue Streams"]
        for action in actions:
            btn = QPushButton(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)
            buttons_layout.addWidget(btn)

        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        return tab

    def create_facilities_tab(self):
        """Create the facilities management tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        # Facilities Overview
        facilities_frame = QFrame()
        facilities_frame.setStyleSheet("background-color: #2a2a2a; border-radius: 10px; padding: 15px;")
        facilities_layout = QVBoxLayout()

        facilities_title = QLabel("Facilities Overview")
        facilities_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        facilities_layout.addWidget(facilities_title)

        # Facility metrics
        facilities = [
            ("Training Center", 85),
            ("Gaming House", 90),
            ("Analysis Room", 80),
            ("Recreation Area", 75),
            ("Medical Facility", 70)
        ]

        self.facility_bars = {}
        for facility, level in facilities:
            facility_layout = QHBoxLayout()
            facility_label = QLabel(facility)
            facility_label.setFixedWidth(150)

            level_progress = QProgressBar()
            level_progress.setValue(level)
            level_progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #333333;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                }
            """)
            self.facility_bars[facility] = level_progress

            facility_layout.addWidget(facility_label)
            facility_layout.addWidget(level_progress)
            facilities_layout.addLayout(facility_layout)

        facilities_frame.setLayout(facilities_layout)
        layout.addWidget(facilities_frame)

        # Facility Management Buttons
        buttons_layout = QHBoxLayout()

        actions = ["Upgrade Facilities", "Manage Staff", "View Maintenance", "Plan Improvements"]
        for action in actions:
            btn = QPushButton(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)
            buttons_layout.addWidget(btn)

        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        return tab

    def create_quick_actions(self):
        """Create the quick actions bar."""
        actions_layout = QHBoxLayout()

        # Create buttons with their actions
        save_btn = QPushButton("Save Game")
        save_btn.clicked.connect(lambda: print("Save game clicked"))  # TODO: Implement save game
        
        team_meeting_btn = QPushButton("Team Meeting")
        team_meeting_btn.clicked.connect(lambda: print("Team meeting clicked"))  # TODO: Implement team meeting
        
        next_match_btn = QPushButton("Next Match")
        next_match_btn.clicked.connect(self.show_next_match)
        
        league_table_btn = QPushButton("League Table")
        league_table_btn.clicked.connect(self.show_league_view)
        
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: print("Settings clicked"))  # TODO: Implement settings
        
        # Style all buttons
        for btn in [save_btn, team_meeting_btn, next_match_btn, league_table_btn, settings_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)
            actions_layout.addWidget(btn)

        return actions_layout
        
    def show_next_match(self):
        """Show the match preview screen for the next match."""
        if not self.game_state or not self.game_state.current_team:
            print("No game state or team available")
            return
        
        if not hasattr(self.game_state, 'league') or not self.game_state.league:
            print("No league available")
            return
            
        # Get all matches involving the player's team
        league = self.game_state.league
        current_team = self.game_state.current_team
        all_matches = []
        
        for division in league.divisions.values():
            team_matches = [
                match for match in division.matches 
                if (match.team1 == current_team or match.team2 == current_team) 
                and not match.result  # Only include unplayed matches
            ]
            all_matches.extend(team_matches)
        
        # Sort matches by date to find the next one
        upcoming_matches = sorted(all_matches, key=lambda m: m.match_date)
        
        if not upcoming_matches:
            print("No upcoming matches")
            return
        
        next_match = upcoming_matches[0]
        self.main_window.show_match_preview(next_match)

    def show_league_view(self):
        """Show the league view screen."""
        self.main_window.show_league_view()
