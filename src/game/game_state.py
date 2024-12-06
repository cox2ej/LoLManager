from datetime import datetime, date
from typing import Dict, List, Optional
from src.models.team import Team
from src.models.player import Player, Role
from src.models.match import Match, MatchResult
from src.models.league import League, Split, SeasonPhase
from src.models.tournament import Tournament
from src.database.db_manager import DatabaseManager

class GameState:
    def __init__(self):
        self.db_manager = None  # Will be set when database is ready
        
        # Core game data
        self.current_team: Optional[Team] = None
        self.current_date = datetime.now()
        self.season = "Spring 2024"
        self.week = 1
        
        # League instances
        self.league: Optional[League] = None  # Player's league
        self.other_leagues: Dict[str, League] = {}  # Other leagues
        
        # League data
        self.standings: Dict[str, Dict] = {}  # team_name -> {wins, losses, points}
        self.schedule: List[Match] = []
        self.match_history: List[MatchResult] = []
        
        # Tournament data
        self.current_tournament: Optional[Tournament] = None
        self.scheduled_tournaments: List[Tournament] = []
        
        # Financial data
        self.sponsorship_income = 0
        self.merchandise_revenue = 0
        self.facility_costs = 0
        self.total_salary = 0
        
        # Facility ratings
        self.facilities = {
            "Training Center": 0,
            "Gaming House": 0,
            "Analysis Room": 0,
            "Recreation Area": 0,
            "Medical Facility": 0
        }
    
    def load_team(self, team_id: int) -> None:
        """Load the player's team and its data."""
        if not self.db_manager:
            return
            
        self.current_team = self.db_manager.load_team(team_id)
        if self.current_team:
            # Load team's roster
            roster = self.db_manager.load_team_roster(team_id)
            for player in roster:
                self.current_team.add_player(player)
            
            # Load or create league
            self.league = self.db_manager.load_league()
            if not self.league:
                # Create a list of all teams
                all_teams = [
                    Team("T1", "Korea", 10000000, 500000, 3, 90, 5000000),
                    Team("Gen.G", "Korea", 8000000, 400000, 2, 85, 4000000),
                    Team("DRX", "Korea", 7000000, 350000, 1, 80, 3500000),
                    Team("KT Rolster", "Korea", 7500000, 380000, 1, 82, 3800000),
                ]
                
                # Add the player's team to the list
                all_teams.append(self.current_team)
                
                # Create league with all teams in the Regular Season division
                divisions = {"Regular Season": all_teams}
                self.league = League("LCK", divisions)
                
                # Start new season
                start_date = datetime.now()
                self.league.start_new_season(Split.SPRING, start_date)
            
            # Calculate financial data
            self.calculate_finances()
    
    def calculate_finances(self) -> None:
        """Calculate current financial status."""
        if not self.current_team:
            return
            
        # Calculate total salary
        self.total_salary = sum(player.salary for role in self.current_team.roster.values() 
                              for player in role)
        
        # Calculate facility costs (based on facility levels)
        self.facility_costs = sum(level * 1000 for level in self.facilities.values())
        
        # Calculate revenue streams (placeholder calculations)
        fanbase = self.current_team.fanbase
        self.sponsorship_income = fanbase * 0.1  # $0.10 per fan per month
        self.merchandise_revenue = fanbase * 0.05  # $0.05 per fan per month
    
    def get_team_performance(self) -> Dict[str, float]:
        """Calculate team's current performance metrics."""
        if not self.current_team or not self.league:
            return {
                "synergy": 0,
                "morale": 0,
                "form": 0,
                "overall": 0
            }
        
        # Calculate team synergy based on communication and leadership
        synergy = sum(
            (player.stats.communication * 0.6 + player.stats.leadership * 0.4) / 100
            for role in self.current_team.roster.values()
            for player in role
        ) / 5  # Average across 5 roles
        
        # Get recent matches
        matches = [m for div in self.league.divisions.values() 
                  for m in (div.matches or [])
                  if m.result and (m.team1 == self.current_team or m.team2 == self.current_team)]
        matches.sort(key=lambda m: m.match_date, reverse=True)
        recent_matches = matches[:5]
        
        # Calculate morale based on recent performance (last 5 matches)
        base_morale = 50
        if recent_matches:
            wins = sum(1 for m in recent_matches if m.result.winner == self.current_team)
            morale = base_morale + (wins / len(recent_matches)) * 50
        else:
            morale = base_morale
        
        # Calculate team form based on overall win rate
        if matches:
            total_wins = sum(1 for m in matches if m.result.winner == self.current_team)
            win_rate = total_wins / len(matches)
            form = 50 + (win_rate * 50)  # Scale win rate to 50-100 range
        else:
            form = 50  # Default form for no matches played
        
        # Calculate overall performance
        overall = (synergy * 0.4 + morale * 0.3 + form * 0.3)
        
        return {
            "synergy": round(synergy, 2),
            "morale": round(morale, 2),
            "form": round(form, 2),
            "overall": round(overall, 2)
        }
    
    def get_recent_results(self) -> List[Dict]:
        """Get recent match results."""
        if not self.current_team or not self.league:
            return []
        matches = [m for div in self.league.divisions.values() 
                  for m in (div.matches or [])
                  if m.result and (m.team1 == self.current_team or m.team2 == self.current_team)]
        matches.sort(key=lambda m: m.match_date, reverse=True)
        return [{
            "date": m.match_date.strftime("%Y-%m-%d"),
            "opponent": (m.team2 if m.team1 == self.current_team else m.team1).name,
            "score": f"{m.result.winner_score}-{m.result.loser_score}",
            "result": "WIN" if m.result.winner == self.current_team else "LOSS"
        } for m in matches[:5]]
    
    def get_upcoming_matches(self) -> List[Dict]:
        """Get upcoming matches."""
        # Placeholder data until match system is implemented
        return [
            {"date": datetime(2024, 1, 20), "opponent": "DRX", "competition": "LCK Spring", "preparation": 85},
            {"date": datetime(2024, 1, 23), "opponent": "Gen.G", "competition": "LCK Spring", "preparation": 70},
            {"date": datetime(2024, 1, 27), "opponent": "T1", "competition": "LCK Spring", "preparation": 60},
            {"date": datetime(2024, 1, 30), "opponent": "KT", "competition": "LCK Spring", "preparation": 75},
            {"date": datetime(2024, 2, 3), "opponent": "DRX", "competition": "LCK Spring", "preparation": 50}
        ]
    
    def get_financial_overview(self) -> Dict[str, str]:
        """Get current financial status."""
        if not self.current_team:
            return {
                "Current Budget": "$0",
                "Total Salary": "$0",
                "Sponsorship Income": "$0/month",
                "Merchandise Revenue": "$0/month",
                "Facility Costs": "$0/month"
            }
            
        return {
            "Current Budget": f"${self.current_team.budget:,}",
            "Total Salary": f"${self.total_salary:,}",
            "Sponsorship Income": f"${self.sponsorship_income:,.0f}/month",
            "Merchandise Revenue": f"${self.merchandise_revenue:,.0f}/month",
            "Facility Costs": f"${self.facility_costs:,}/month"
        }
    
    def get_facility_levels(self) -> Dict[str, int]:
        """Get current facility levels."""
        if not self.current_team:
            return self.facilities
            
        # Update facilities based on team data
        self.facilities = {
            "Training Center": self.current_team.training_facilities,
            "Gaming House": 80,  # Placeholder values
            "Analysis Room": 75,
            "Recreation Area": 70,
            "Medical Facility": 65
        }
        return self.facilities

    def schedule_tournament(self, name: str, start_date: datetime, participating_leagues: Optional[List[League]] = None) -> None:
        """Schedule a new tournament."""
        if participating_leagues is None:
            # Default to all leagues including player's league
            participating_leagues = list(self.other_leagues.values())
            if self.league:
                participating_leagues.append(self.league)
        
        tournament = Tournament(name, participating_leagues, start_date)
        self.scheduled_tournaments.append(tournament)
        
    def update_tournaments(self) -> None:
        """Update tournament states and progress."""
        current_date = self.current_date
        
        # Check if we need to start a new tournament
        if not self.current_tournament and self.scheduled_tournaments:
            next_tournament = self.scheduled_tournaments[0]
            if current_date >= next_tournament.start_date:
                self.current_tournament = next_tournament
                self.scheduled_tournaments.pop(0)
                self.current_tournament.initialize_tournament()
        
        # Update current tournament if exists
        if self.current_tournament:
            if self.current_tournament.current_phase == "Group Stage":
                # Simulate pending group stage matches for current date
                pending_matches = [m for m in self.current_tournament.group_stage_matches 
                                 if not m.result and m.date <= current_date]
                for match in pending_matches:
                    match.simulate()
                    self.current_tournament.update_group_standings(match)
                
                # Check if group stage is complete
                if all(m.result for m in self.current_tournament.group_stage_matches):
                    self.current_tournament.start_knockout_stage()
            
            elif self.current_tournament.current_phase == "Knockout Stage":
                # Simulate pending knockout matches for current date
                pending_matches = [m for m in self.current_tournament.knockout_matches 
                                 if not m.result and m.date <= current_date]
                for match in pending_matches:
                    match.simulate()
                    self.current_tournament.update_knockout_stage(match)
                
                # Check if tournament is complete
                if all(m.result for m in self.current_tournament.knockout_matches):
                    self.current_tournament.current_phase = "Finished"
                    self.award_tournament_rewards()
                    self.current_tournament = None

    def award_tournament_rewards(self) -> None:
        """Award prizes and championship points for tournament performance."""
        if not self.current_tournament or self.current_tournament.current_phase != "Finished":
            return
            
        # Award championship points based on tournament performance
        points_distribution = {
            "winner": 100,
            "runner_up": 70,
            "semi_finalist": 40,
            "quarter_finalist": 20,
            "group_stage": 10
        }
        
        # Award points to winner and runner-up
        final_match = self.current_tournament.knockout_matches[-1]
        winner = final_match.result.winner
        runner_up = final_match.result.loser
        
        winner.championship_points += points_distribution["winner"]
        runner_up.championship_points += points_distribution["runner_up"]
        
        # Award points to semi-finalists
        semi_finals = self.current_tournament.knockout_matches[-3:-1]
        for match in semi_finals:
            match.result.loser.championship_points += points_distribution["semi_finalist"]
        
        # Award points to quarter-finalists
        quarter_finals = self.current_tournament.knockout_matches[:-3]
        for match in quarter_finals:
            match.result.loser.championship_points += points_distribution["quarter_finalist"]
        
        # Award points to teams that made it out of groups but lost in quarters
        for group in self.current_tournament.groups.values():
            for team in group:
                if team not in [winner, runner_up] and \
                   not any(m.result.loser == team for m in semi_finals) and \
                   not any(m.result.loser == team for m in quarter_finals):
                    team.championship_points += points_distribution["group_stage"]
        
        # Award prize money (example values)
        prize_pool = 1000000  # $1M prize pool
        prize_distribution = {
            "winner": 0.5,  # 50% of prize pool
            "runner_up": 0.25,  # 25% of prize pool
            "semi_finalist": 0.1,  # 10% each (20% total)
            "quarter_finalist": 0.0125  # 1.25% each (5% total)
        }
        
        # Distribute prize money
        winner.budget += prize_pool * prize_distribution["winner"]
        runner_up.budget += prize_pool * prize_distribution["runner_up"]
        
        for match in semi_finals:
            match.result.loser.budget += prize_pool * prize_distribution["semi_finalist"]
            
        for match in quarter_finals:
            match.result.loser.budget += prize_pool * prize_distribution["quarter_finalist"]

    def simulate_all_leagues(self) -> Dict[str, Dict[str, List[MatchResult]]]:
        """Simulate matches for all leagues and tournaments."""
        all_results = {}
        
        # First check if any leagues need to start playoffs
        if self.league and self.league.current_season.phase == SeasonPhase.REGULAR_SEASON:
            if self.league.is_regular_season_finished():
                self.league.start_playoffs()
                
        for league in self.other_leagues.values():
            if league.current_season.phase == SeasonPhase.REGULAR_SEASON:
                if league.is_regular_season_finished():
                    league.start_playoffs()
        
        # Then simulate matches for all leagues
        if self.league:
            if self.league.current_season.phase == SeasonPhase.REGULAR_SEASON:
                all_results[self.league.name] = self.league.simulate_week(player_team=self.current_team)
            elif self.league.current_season.phase == SeasonPhase.PLAYOFFS:
                playoffs_complete = self.league.simulate_playoff_round()
                playoff_div = self.league.divisions.get("Playoffs")
                if playoff_div:
                    all_results[self.league.name] = {"Playoffs": [m.result for m in playoff_div.matches if m.result]}
            
        # Simulate other leagues
        for league_name, league in self.other_leagues.items():
            if league.current_season.phase == SeasonPhase.REGULAR_SEASON:
                all_results[league_name] = league.simulate_week()
            elif league.current_season.phase == SeasonPhase.PLAYOFFS:
                playoffs_complete = league.simulate_playoff_round()
                playoff_div = league.divisions.get("Playoffs")
                if playoff_div:
                    all_results[league_name] = {"Playoffs": [m.result for m in playoff_div.matches if m.result]}
                    
        # Update tournaments
        self.update_tournaments()  # Check if any tournaments should start
        if self.current_tournament:
            self.update_tournaments()
            
        return all_results

    def get_league_position(self) -> str:
        """Get current team's position in the league."""
        if not self.current_team or not self.league:
            return "N/A"
            
        # Get all teams in the current division
        current_division = None
        for division in self.league.divisions.values():
            if self.current_team in division.teams:
                current_division = division
                break
                
        if not current_division:
            return "N/A"
            
        # Calculate standings for each team
        standings = []
        for team in current_division.teams:
            team_matches = [m for m in current_division.matches 
                          if m.result and (m.team1 == team or m.team2 == team)]
            wins = sum(1 for m in team_matches if m.result.winner == team)
            losses = sum(1 for m in team_matches if m.result and m.result.winner != team)
            win_rate = wins / len(team_matches) if team_matches else 0
            
            standings.append({
                'team': team,
                'wins': wins,
                'losses': losses,
                'win_rate': win_rate
            })
        
        # Sort by wins (descending) then win rate (descending)
        standings.sort(key=lambda x: (-x['wins'], -x['win_rate']))
        
        # Find current team's position
        for i, standing in enumerate(standings):
            if standing['team'] == self.current_team:
                position = i + 1
                suffix = 'th' if 11 <= position <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(position % 10, 'th')
                return f"{position}{suffix}"
        
        return "N/A"
    
    def get_win_rate(self) -> float:
        """Calculate win rate from actual match results."""
        if not self.current_team or not self.league:
            return 0.0
            
        # Get all matches from all divisions involving the current team
        matches = [m for div in self.league.divisions.values() 
                  for m in (div.matches or [])
                  if m.result and (m.team1 == self.current_team or m.team2 == self.current_team)]
        
        if not matches:
            return 0.0
            
        wins = sum(1 for m in matches if m.result.winner == self.current_team)
        return (wins / len(matches)) * 100
