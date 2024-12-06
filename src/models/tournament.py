from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

from .team import Team
from .match import Match, MatchResult
from .league import League


class Tournament:
    def __init__(self, name: str, participating_leagues: List[League], start_date: datetime):
        self.name = name
        self.participating_leagues = participating_leagues
        self.start_date = start_date
        self.teams: List[Team] = []
        self.group_stage_matches: List[Match] = []
        self.knockout_matches: List[Match] = []
        self.current_phase = "Not Started"  # Not Started, Group Stage, Knockout Stage, Finished
        self.groups: Dict[str, List[Team]] = {}  # Group name -> List of teams
        self.group_standings: Dict[str, List[Dict]] = {}  # Group name -> List of team stats
        self.winner: Optional[Team] = None

    def initialize_tournament(self, teams_per_league: int = 4):
        """Initialize tournament with top teams from each league."""
        self.teams = []
        for league in self.participating_leagues:
            qualified_teams = league.get_playoff_teams()[:teams_per_league]
            self.teams.extend([team for _, team in qualified_teams])

        # Create groups (assuming 4 groups)
        num_groups = 4
        teams_per_group = len(self.teams) // num_groups
        
        # Randomly assign teams to groups
        shuffled_teams = self.teams.copy()
        random.shuffle(shuffled_teams)
        
        for i in range(num_groups):
            group_name = chr(65 + i)  # A, B, C, D
            start_idx = i * teams_per_group
            end_idx = start_idx + teams_per_group
            self.groups[group_name] = shuffled_teams[start_idx:end_idx]
            
            # Initialize standings for this group
            self.group_standings[group_name] = [
                {"team": team, "wins": 0, "losses": 0, "game_diff": 0} 
                for team in self.groups[group_name]
            ]

        self.schedule_group_stage()
        self.current_phase = "Group Stage"

    def schedule_group_stage(self):
        """Schedule round-robin matches within each group."""
        current_date = self.start_date
        for group_name, group_teams in self.groups.items():
            # Create round-robin schedule
            for i in range(len(group_teams)):
                for j in range(i + 1, len(group_teams)):
                    match = Match(group_teams[i], group_teams[j], current_date)
                    self.group_stage_matches.append(match)
                    current_date += timedelta(days=1)

    def update_group_standings(self, completed_match: Match):
        """Update group standings after a match is completed."""
        if self.current_phase != "Group Stage":
            return

        # Find which group this match belongs to
        target_group = None
        for group_name, group_teams in self.groups.items():
            if completed_match.team1 in group_teams and completed_match.team2 in group_teams:
                target_group = group_name
                break

        if not target_group:
            return

        # Update standings
        winner = completed_match.result.winner
        loser = completed_match.team2 if winner == completed_match.team1 else completed_match.team1
        
        for team_stats in self.group_standings[target_group]:
            if team_stats["team"] == winner:
                team_stats["wins"] += 1
                team_stats["game_diff"] += completed_match.result.game_differential
            elif team_stats["team"] == loser:
                team_stats["losses"] += 1
                team_stats["game_diff"] -= completed_match.result.game_differential

    def start_knockout_stage(self):
        """Start the knockout stage with top 2 teams from each group."""
        if self.current_phase != "Group Stage":
            return

        # Get top 2 teams from each group
        qualified_teams = []
        for group_name in self.groups:
            sorted_standings = sorted(
                self.group_standings[group_name],
                key=lambda x: (-x["wins"], -x["game_diff"])
            )
            qualified_teams.extend([stats["team"] for stats in sorted_standings[:2]])

        # Create quarter-final matches
        current_date = max(match.date for match in self.group_stage_matches) + timedelta(days=2)
        for i in range(0, len(qualified_teams), 2):
            match = Match(qualified_teams[i], qualified_teams[i+1], current_date)
            self.knockout_matches.append(match)
            current_date += timedelta(days=1)

        self.current_phase = "Knockout Stage"

    def update_knockout_stage(self, completed_match: Match):
        """Update knockout stage bracket after a match is completed."""
        if self.current_phase != "Knockout Stage":
            return

        remaining_matches = [m for m in self.knockout_matches if not m.result]
        if not remaining_matches:
            # Tournament is finished
            self.winner = completed_match.result.winner
            self.current_phase = "Finished"
            return

        # Schedule next round match if needed
        if len(remaining_matches) == 2:  # Time for semi-finals
            match = Match(completed_match.result.winner, None,
                        completed_match.date + timedelta(days=2))
            self.knockout_matches.append(match)
        elif len(remaining_matches) == 1:  # Time for finals
            match = Match(completed_match.result.winner, None,
                        completed_match.date + timedelta(days=3))
            self.knockout_matches.append(match)
