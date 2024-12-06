from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .team import Team

class ObjectiveType(Enum):
    TOWER = "Tower"
    DRAGON = "Dragon"
    BARON = "Baron"
    INHIBITOR = "Inhibitor"

@dataclass
class ObjectiveTradeEvent:
    """Represents an objective trade between teams."""
    team1: Team
    team2: Team
    team1_objective: ObjectiveType
    team2_objective: ObjectiveType
    team1_location: str
    team2_location: str
    time: int

    def get_trade_value_ratio(self) -> float:
        """Calculate the value ratio of the trade (team1:team2)."""
        objective_values = {
            ObjectiveType.TOWER: 1.0,
            ObjectiveType.DRAGON: 1.2,
            ObjectiveType.BARON: 2.0,
            ObjectiveType.INHIBITOR: 1.5
        }
        team1_value = objective_values[self.team1_objective]
        team2_value = objective_values[self.team2_objective]
        return team1_value / team2_value

    def get_winner(self) -> Optional[Team]:
        """Determine if one team got a significantly better trade."""
        ratio = self.get_trade_value_ratio()
        if ratio > 1.2:  # Team 1 got significantly better trade
            return self.team1
        elif ratio < 0.8:  # Team 2 got significantly better trade
            return self.team2
        return None  # Even trade

    def get_description(self) -> str:
        """Generate a description of the objective trade."""
        team1_obj = f"{self.team1_objective.value} in {self.team1_location}"
        team2_obj = f"{self.team2_objective.value} in {self.team2_location}"
        
        winner = self.get_winner()
        if winner == self.team1:
            return f"{self.team1.name} trades up, securing {team1_obj} while {self.team2.name} takes {team2_obj}"
        elif winner == self.team2:
            return f"{self.team2.name} gets the better trade, taking {team2_obj} while {self.team1.name} secures {team1_obj}"
        else:
            return f"Even trade as {self.team1.name} takes {team1_obj} while {self.team2.name} secures {team2_obj}"
