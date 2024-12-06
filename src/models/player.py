from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class Role(Enum):
    TOP = "Top"
    JUNGLE = "Jungle"
    MID = "Mid"
    ADC = "ADC"
    SUPPORT = "Support"


@dataclass
class PlayerStats:
    mechanical_skill: int  # 1-100
    game_knowledge: int   # 1-100
    communication: int    # 1-100
    leadership: int      # 1-100
    
    @property
    def overall_rating(self) -> float:
        """Calculate player's overall rating based on their stats."""
        weights = {
            'mechanical_skill': 0.35,
            'game_knowledge': 0.35,
            'communication': 0.15,
            'leadership': 0.15
        }
        
        rating = (
            self.mechanical_skill * weights['mechanical_skill'] +
            self.game_knowledge * weights['game_knowledge'] +
            self.communication * weights['communication'] +
            self.leadership * weights['leadership']
        )
        return round(rating, 2)


class Player:
    def __init__(
        self,
        name: str,
        role: Role,
        stats: PlayerStats,
        nationality: str,
        salary: int,
        contract_end: date,
        team_id: Optional[int] = None
    ):
        self.name = name
        self.role = role
        self.stats = stats
        self.nationality = nationality
        self.salary = salary
        self.contract_end = contract_end
        self.team_id = team_id
        
        # Performance tracking
        self.games_played = 0
        self.wins = 0
        self.losses = 0
    
    @property
    def win_rate(self) -> float:
        """Calculate player's win rate."""
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100
    
    def update_performance(self, won: bool):
        """Update player's performance statistics after a match."""
        self.games_played += 1
        if won:
            self.wins += 1
        else:
            self.losses += 1
    
    def is_contract_expired(self, current_date: date) -> bool:
        """Check if player's contract has expired."""
        return current_date >= self.contract_end
    
    def __str__(self) -> str:
        return (
            f"{self.name} ({self.role.value}) - "
            f"Rating: {self.stats.overall_rating:.1f} - "
            f"Win Rate: {self.win_rate:.1f}%"
        )
    
    def __eq__(self, other) -> bool:
        """Compare players based on their name and role."""
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.role == other.role
    
    def __hash__(self) -> int:
        """Hash player based on name and role."""
        return hash((self.name, self.role))
