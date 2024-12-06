from typing import Dict, List, Optional
from .player import Player, Role


class TeamError(Exception):
    """Custom exception for team-related errors."""
    pass


class Team:
    def __init__(
        self,
        name: str,
        region: str,
        budget: int,
        team_id: Optional[int] = None,
        fanbase: int = 0,
        championships: int = 0,
        training_facilities: int = 0,
        brand_value: int = 0
    ):
        self.name = name
        self.region = region
        self.budget = budget
        self.team_id = team_id
        self.fanbase = fanbase
        self.championships = championships
        self.training_facilities = training_facilities
        self.brand_value = brand_value
        
        # Initialize empty roster
        self.roster: Dict[Role, List[Player]] = {
            role: [] for role in Role
        }
        
        # Performance tracking
        self.wins = 0
        self.losses = 0
        self.championship_points = 0
        self.game_differential = 0  # For tiebreaker calculations
        self.current_streak = 0  # Positive for win streak, negative for loss streak
        self.season_history = []  # Track performance across seasons
        self.world_championships = 0
        self.domestic_titles = 0
    
    @property
    def win_rate(self) -> float:
        """Calculate team's win rate."""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return self.wins / total_games

    def get_strength(self) -> float:
        """Calculate team's overall strength based on various factors."""
        # Base strength from win rate (40%)
        strength = self.win_rate * 40
        
        # Add strength from training facilities (20%)
        strength += (self.training_facilities / 100) * 20
        
        # Add strength from championships (20%)
        championship_factor = min(1.0, (self.championships + self.world_championships) / 5)
        strength += championship_factor * 20
        
        # Add strength from current streak (20%)
        streak_factor = max(-1.0, min(1.0, self.current_streak / 5))  # Cap at ±5 games
        streak_contribution = 10 + (streak_factor * 10)  # Range from 0-20
        strength += streak_contribution
        
        return strength
    
    @property
    def players(self) -> List[Player]:
        """Get all players in the team's roster."""
        all_players = []
        for role_players in self.roster.values():
            all_players.extend(role_players)
        return all_players
    
    def add_player(self, player: Player) -> None:
        """Add a player to the team's roster."""
        # Update player's team
        player.team_id = self.team_id
        
        # Add to roster
        self.roster[player.role].append(player)
    
    def remove_player(self, player: Player) -> None:
        """Remove a player from the team's roster."""
        if player in self.roster[player.role]:
            self.roster[player.role].remove(player)
            player.team_id = None
    
    def get_starting_lineup(self) -> Dict[Role, Optional[Player]]:
        """Get the best player for each role based on overall rating."""
        lineup = {}
        for role in Role:
            players = self.roster[role]
            if not players:
                lineup[role] = None
            else:
                # Get player with highest rating
                lineup[role] = max(
                    players,
                    key=lambda p: p.stats.overall_rating
                )
        return lineup
    
    def is_roster_valid(self) -> bool:
        """Check if team has at least one player in each role."""
        return all(len(players) > 0 for players in self.roster.values())
    
    def get_total_salary(self) -> int:
        """Calculate total salary expenses."""
        return sum(
            player.salary
            for role_players in self.roster.values()
            for player in role_players
        )
    
    def get_roster_strength(self) -> float:
        """Calculate overall team strength based on starting lineup."""
        lineup = self.get_starting_lineup()
        if not all(lineup.values()):
            return 0.0
        
        return sum(
            player.stats.overall_rating
            for player in lineup.values()
            if player is not None
        ) / len(Role)
    
    def update_performance(self, won: bool) -> None:
        """Update team's performance after a match."""
        if won:
            self.wins += 1
        else:
            self.losses += 1
        
        # Update all players in starting lineup
        lineup = self.get_starting_lineup()
        for player in lineup.values():
            if player:
                player.update_performance(won)
    
    def reset_stats(self) -> None:
        """Reset team's seasonal stats."""
        # Archive current season stats
        if self.wins > 0 or self.losses > 0:
            self.season_history.append({
                'wins': self.wins,
                'losses': self.losses,
                'points': self.championship_points,
                'game_diff': self.game_differential,
            })
        
        # Reset current stats
        self.wins = 0
        self.losses = 0
        self.championship_points = 0
        self.game_differential = 0
        self.current_streak = 0
    
    def update_match_stats(self, won: bool, score_diff: int):
        """Update team stats after a match.
        
        Args:
            won: Whether the team won the match
            score_diff: Score differential (positive for winner, negative for loser)
        """
        if won:
            self.wins += 1
            if self.current_streak >= 0:
                self.current_streak += 1  # Extend win streak
            else:
                self.current_streak = 1  # Start new win streak
        else:
            self.losses += 1
            if self.current_streak <= 0:
                self.current_streak -= 1  # Extend loss streak
            else:
                self.current_streak = -1  # Start new loss streak
        
        self.game_differential += score_diff

    def update_stats_after_match(self, won: bool, score_diff: int) -> None:
        """Update team stats after a match."""
        if won:
            self.wins += 1
            self.current_streak = max(1, self.current_streak + 1)
        else:
            self.losses += 1
            self.current_streak = min(-1, self.current_streak - 1)
        
        self.game_differential += score_diff
    
    def award_championship(self, is_worlds: bool = False) -> None:
        """Award championship title to team."""
        if is_worlds:
            self.world_championships += 1
            self.championship_points += 1000  # Worlds gives massive points
        else:
            self.domestic_titles += 1
            self.championship_points += 100  # Domestic title points
        
        # Increase brand value and fanbase
        self.brand_value += 5000
        self.fanbase += 10000
    
    def __eq__(self, other):
        """Compare teams by name and region."""
        if not isinstance(other, Team):
            return False
        return self.name == other.name and self.region == other.region
    
    def __hash__(self):
        """Hash based on name and region."""
        return hash((self.name, self.region))
    
    def __str__(self) -> str:
        return (
            f"{self.name} ({self.region}) - "
            f"Win Rate: {self.win_rate:.1f}% - "
            f"Roster Strength: {self.get_roster_strength():.1f}"
        )
