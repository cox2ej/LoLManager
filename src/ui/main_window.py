from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from src.ui.screens.title_screen import TitleScreen
from src.ui.screens.new_game_screen import NewGameScreen
from src.ui.screens.load_game_screen import LoadGameScreen
from src.ui.screens.settings_screen import SettingsScreen
from src.ui.screens.team_setup_screen import TeamSetupScreen
from src.ui.screens.main_hub_screen import MainHubScreen
from src.ui.screens.match_preview_screen import MatchPreviewScreen
from src.ui.screens.match_simulation_screen import MatchSimulationScreen
from src.ui.screens.draft_screen import DraftScreen
from src.ui.screens.league_view import LeagueView
from src.game.game_state import GameState
from src.models.match import Match


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("League of Legends Manager")
        self.setMinimumSize(1024, 768)  # Set minimum window size
        
        # Initialize game state
        self.game_state = GameState()
        print("Game state initialized")  # Debug print
        
        # Initialize player's team
        self.player_team = None
        
        # Create stacked widget to manage different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.title_screen = TitleScreen(self)
        self.new_game_screen = NewGameScreen(self)
        self.load_game_screen = LoadGameScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.team_setup_screen = None  # Will be initialized when needed
        self.main_hub_screen = None  # Will be initialized when needed
        self.draft_screen = None  # Will be initialized when needed
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.title_screen)
        self.stacked_widget.addWidget(self.new_game_screen)
        self.stacked_widget.addWidget(self.load_game_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        
        # Show title screen by default
        self.stacked_widget.setCurrentWidget(self.title_screen)
        print("Showing title screen")  # Debug print
        
        # Center the window on the screen
        self.center_window()
    
    def center_window(self):
        """Center the main window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def show_title_screen(self):
        """Switch to title screen."""
        print("Showing title screen")  # Debug print
        self.stacked_widget.setCurrentWidget(self.title_screen)
    
    def show_new_game_screen(self):
        """Switch to new game screen."""
        print("Showing new game screen")  # Debug print
        self.stacked_widget.setCurrentWidget(self.new_game_screen)
    
    def show_load_game_screen(self):
        """Switch to load game screen."""
        print("Showing load game screen")  # Debug print
        self.stacked_widget.setCurrentWidget(self.load_game_screen)
    
    def show_settings_screen(self):
        """Switch to settings screen."""
        print("Showing settings screen")  # Debug print
        self.stacked_widget.setCurrentWidget(self.settings_screen)
    
    def show_team_setup_screen(self, selected_region):
        """Initialize and show the team setup screen with the selected region."""
        print(f"Showing team setup screen for region: {selected_region}")  # Debug print
        
        # Remove existing team setup screen if it exists
        if self.team_setup_screen:
            self.stacked_widget.removeWidget(self.team_setup_screen)
            self.team_setup_screen.deleteLater()
        
        # Create new team setup screen with selected region
        self.team_setup_screen = TeamSetupScreen(self, selected_region)
        self.stacked_widget.addWidget(self.team_setup_screen)
        self.stacked_widget.setCurrentWidget(self.team_setup_screen)
    
    def show_main_hub_screen(self):
        """Switch to main hub screen."""
        print(f"Showing main hub screen. Current team: {self.game_state.current_team.name if self.game_state.current_team else 'None'}")  # Debug print
        
        # Remove existing main hub screen if it exists
        if self.main_hub_screen:
            self.stacked_widget.removeWidget(self.main_hub_screen)
            self.main_hub_screen.deleteLater()
        
        # Create new main hub screen with current game state
        self.main_hub_screen = MainHubScreen(self, self.game_state)
        self.stacked_widget.addWidget(self.main_hub_screen)
        self.stacked_widget.setCurrentWidget(self.main_hub_screen)
    
    def show_match_preview(self, match: Match):
        """Show the match preview screen."""
        match_preview = MatchPreviewScreen(self, match)
        match_preview.match_started.connect(self.show_match_simulation)
        match_preview.draft_started.connect(self.show_draft_screen)  # Connect new signal
        
        self.stacked_widget.addWidget(match_preview)
        self.stacked_widget.setCurrentWidget(match_preview)

    def show_draft_screen(self, match: Match, team1_is_blue: bool):
        """Show the draft screen."""
        # Initialize draft state with correct team sides
        draft_state = match.start_draft(team1_is_blue)
        
        # Create and show draft screen
        self.draft_screen = DraftScreen(draft_state, self)
        self.draft_screen.draft_completed.connect(lambda state: self.handle_draft_completion(match))
        
        self.stacked_widget.addWidget(self.draft_screen)
        self.stacked_widget.setCurrentWidget(self.draft_screen)
    
    def handle_draft_completion(self, match: Match):
        """Handle completion of draft phase."""
        # Remove draft screen
        if self.draft_screen:
            self.stacked_widget.removeWidget(self.draft_screen)
            self.draft_screen = None
        
        # Show match simulation screen
        self.show_match_simulation(match)
    
    def show_match_simulation(self, match: Match):
        """Show the match simulation screen."""
        # Remove existing main hub screen
        if self.main_hub_screen:
            self.stacked_widget.removeWidget(self.main_hub_screen)
            self.main_hub_screen.deleteLater()
            self.main_hub_screen = None
            
        # Create and show match simulation screen
        match_simulation_screen = MatchSimulationScreen(self, match)
        self.stacked_widget.addWidget(match_simulation_screen)
        self.stacked_widget.setCurrentWidget(match_simulation_screen)
        
        # Connect match completed signal
        match_simulation_screen.match_completed.connect(self.show_match_result)
    
    def show_match_result(self, match: Match):
        """Show the match result screen."""
        # TODO: Implement match result screen
        print(f"Match completed: {match.result.winner.name} defeats {match.result.loser.name} {match.result.winner_score}-{match.result.loser_score}")
        
        # Remove match simulation screen
        simulation_screen = self.stacked_widget.currentWidget()
        self.stacked_widget.removeWidget(simulation_screen)
        simulation_screen.deleteLater()
        
        # Update league view if it exists
        league_view = self.findChild(LeagueView)
        if league_view:
            league_view.update_view()
        
        # Show main hub screen
        self.show_main_hub_screen()
    
    def show_league_view(self):
        """Show the league view screen."""
        from src.ui.screens.league_view import LeagueView
        league_view = LeagueView(self.game_state.league, self)
        
        # Remove any existing league view
        current_league_view = self.findChild(LeagueView)
        if current_league_view:
            self.stacked_widget.removeWidget(current_league_view)
            current_league_view.deleteLater()
        
        self.stacked_widget.addWidget(league_view)
        self.stacked_widget.setCurrentWidget(league_view)
    
    def clear_current_screen(self):
        """Clear the current screen and clean up."""
        current = self.stacked_widget.currentWidget()
        if current:
            self.stacked_widget.removeWidget(current)
            current.deleteLater()

    def start_league(self, league):
        """Initialize the game state with the league and show the main hub screen."""
        # Set player's league
        self.game_state.league = league
        self.game_state.current_team = self.player_team  # Use the player's selected team

        # Initialize other leagues based on player's league
        if league.name == "LCK":
            # Add LEC, LPL, and LCS
            from src.data.lec_teams import create_lec_league
            from src.data.lpl_teams import create_lpl_league
            from src.data.lcs_teams import create_lcs_league
            self.game_state.other_leagues["LEC"] = create_lec_league()
            self.game_state.other_leagues["LPL"] = create_lpl_league()
            self.game_state.other_leagues["LCS"] = create_lcs_league()
        elif league.name == "LEC":
            # Add LCK, LPL, and LCS
            from src.data.lck_teams import create_lck_league
            from src.data.lpl_teams import create_lpl_league
            from src.data.lcs_teams import create_lcs_league
            self.game_state.other_leagues["LCK"] = create_lck_league()
            self.game_state.other_leagues["LPL"] = create_lpl_league()
            self.game_state.other_leagues["LCS"] = create_lcs_league()
        elif league.name == "LPL":
            # Add LCK, LEC, and LCS
            from src.data.lck_teams import create_lck_league
            from src.data.lec_teams import create_lec_league
            from src.data.lcs_teams import create_lcs_league
            self.game_state.other_leagues["LCK"] = create_lck_league()
            self.game_state.other_leagues["LEC"] = create_lec_league()
            self.game_state.other_leagues["LCS"] = create_lcs_league()
        elif league.name == "LCS":
            # Add LCK, LEC, and LPL
            from src.data.lck_teams import create_lck_league
            from src.data.lec_teams import create_lec_league
            from src.data.lpl_teams import create_lpl_league
            self.game_state.other_leagues["LCK"] = create_lck_league()
            self.game_state.other_leagues["LEC"] = create_lec_league()
            self.game_state.other_leagues["LPL"] = create_lpl_league()

        # Start new season for all leagues
        from datetime import datetime
        from src.models.league import Split
        
        # Use the same start date and split for all leagues
        start_date = datetime(2024, 1, 15)  # Start on January 15th, 2024
        split = Split.SPRING  # Start with Spring split
        
        if self.game_state.league:
            self.game_state.league.start_new_season(split, start_date)
        for league in self.game_state.other_leagues.values():
            league.start_new_season(split, start_date)

        self.show_main_hub_screen()
