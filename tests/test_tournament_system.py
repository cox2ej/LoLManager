import unittest
from datetime import datetime, timedelta
from src.models.team import Team
from src.models.league import League, Split, SeasonPhase
from src.models.tournament import Tournament
from src.game.game_state import GameState
from src.data.lck_teams import create_lck_league
from src.data.lpl_teams import create_lpl_league
from src.data.lec_teams import create_lec_league
from src.data.lcs_teams import create_lcs_league

class TestTournamentSystem(unittest.TestCase):
    def setUp(self):
        """Set up test data using actual game functions."""
        # Initialize GameState
        self.game_state = GameState()
        
        # Create all major leagues using existing functions
        self.lck = create_lck_league()
        self.lpl = create_lpl_league()
        self.lec = create_lec_league()
        self.lcs = create_lcs_league()
        
        # Set LCK as the player's league and others as other leagues
        self.game_state.league = self.lck
        self.game_state.other_leagues = {
            "LPL": self.lpl,
            "LEC": self.lec,
            "LCS": self.lcs
        }
        
        # Set current date and start seasons for all leagues
        self.game_state.current_date = datetime(2024, 1, 15)  # Start on January 15th, 2024
        start_date = self.game_state.current_date
        
        # Start seasons for all leagues
        for league in [self.lck, self.lpl, self.lec, self.lcs]:
            league.start_new_season(Split.SPRING, start_date)

    def test_playoff_system(self):
        """Test the playoff system for all leagues."""
        # Simulate regular season until all leagues reach playoffs
        max_weeks = 12  # Maximum number of weeks to simulate
        weeks_simulated = 0
        
        while weeks_simulated < max_weeks and not all(
            league.current_season.phase == SeasonPhase.PLAYOFFS 
            for league in [self.lck, self.lpl, self.lec, self.lcs]
        ):
            self.game_state.simulate_all_leagues()
            self.game_state.current_date += timedelta(days=7)
            weeks_simulated += 1
        
        # Verify playoffs started in all leagues
        for league in [self.lck, self.lpl, self.lec, self.lcs]:
            self.assertEqual(league.current_season.phase, SeasonPhase.PLAYOFFS)
            
            # Get playoff teams and verify count
            playoff_teams = league.get_playoff_teams()
            self.assertEqual(len(playoff_teams), 6)  # Top 6 teams make playoffs
            
            # Print playoff teams for verification
            print(f"\n{league.name} Playoff Teams:")
            for seed, team in playoff_teams:
                print(f"Seed {seed}: {team.name}")
        
        # Simulate playoffs with a maximum duration
        max_playoff_days = 30  # Maximum days to simulate playoffs
        days_simulated = 0
        
        while days_simulated < max_playoff_days and any(
            league.current_season.phase == SeasonPhase.PLAYOFFS
            for league in [self.lck, self.lpl, self.lec, self.lcs]
        ):
            self.game_state.simulate_all_leagues()
            self.game_state.current_date += timedelta(days=1)
            days_simulated += 1
        
        # Verify champions
        for league in [self.lck, self.lpl, self.lec, self.lcs]:
            champion = league.get_champion()
            self.assertIsNotNone(champion)
            print(f"\n{league.name} Champion: {champion.name}")

    def test_tournament_system(self):
        """Test the tournament system with all major regions."""
        # Schedule MSI-style tournament
        tournament_start = self.game_state.current_date + timedelta(days=14)
        self.game_state.schedule_tournament(
            "Mid-Season Invitational 2024",
            tournament_start
        )
        
        # Verify tournament was scheduled
        self.assertEqual(len(self.game_state.scheduled_tournaments), 1)
        
        # Simulate until tournament completion with a maximum duration
        max_tournament_days = 30  # Maximum days to simulate
        days_simulated = 0
        
        while days_simulated < max_tournament_days and (
            self.game_state.current_tournament or 
            (self.game_state.scheduled_tournaments and 
             self.game_state.current_date < tournament_start)
        ):
            self.game_state.simulate_all_leagues()
            self.game_state.current_date += timedelta(days=1)
            days_simulated += 1
            
            # Print tournament progress
            if self.game_state.current_tournament:
                tournament = self.game_state.current_tournament
                stats = tournament.get_tournament_stats()
                
                print(f"\nTournament Phase: {stats['phase']}")
                
                if stats['phase'] == "Group Stage":
                    for group_name, group_stats in stats['groups'].items():
                        print(f"\nGroup {group_name}:")
                        for team_stat in group_stats:
                            print(f"{team_stat['team'].name}: "
                                  f"{team_stat['wins']}W-{team_stat['losses']}L "
                                  f"({team_stat['points']} pts)")
                
                elif stats['phase'] == "Knockout Stage":
                    print("\nKnockout Stage Matches:")
                    for match in stats['knockout_stage']:
                        if match['completed']:
                            print(f"{match['team1'].name} vs {match['team2'].name}: "
                                  f"{match['score']} - Winner: {match['winner'].name}")
                        else:
                            print(f"Upcoming: {match['team1'].name} vs {match['team2'].name}")
        
        # Verify tournament completed within time limit
        self.assertLess(days_simulated, max_tournament_days, 
                       "Tournament simulation exceeded maximum duration")
        
        # Verify championship points distribution
        print("\nFinal Championship Points:")
        all_teams = []
        for league in [self.lck, self.lpl, self.lec, self.lcs]:
            all_teams.extend(league.get_all_teams())
            
        for team in sorted(all_teams, key=lambda x: x.championship_points, reverse=True):
            if team.championship_points > 0:
                print(f"{team.name}: {team.championship_points} points")

if __name__ == '__main__':
    unittest.main()
