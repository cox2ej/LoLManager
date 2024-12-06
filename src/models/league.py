from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random

from .team import Team
from .match import Match, MatchResult


class SeasonPhase(Enum):
    REGULAR_SEASON = "Regular Season"
    PLAYOFFS = "Playoffs"
    OFF_SEASON = "Off Season"


class Split(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"


class Division:
    def __init__(self, name: str, teams: List[Team]):
        self.name = name
        self.teams = teams
        self.matches: List[Match] = []

    def get_standings(self) -> List[Dict]:
        """Get division standings with detailed stats."""
        standings = []
        for team in self.teams:
            # Initialize stats
            wins = 0
            losses = 0
            game_diff = 0
            current_streak = 0
            streak_type = None  # None = no streak, True = win streak, False = loss streak
            
            # Calculate head-to-head records
            h2h_records = {}
            for other_team in self.teams:
                if other_team != team:
                    h2h_records[other_team.name] = {
                        'wins': 0,
                        'losses': 0
                    }

            # Calculate matches against each team
            for match in sorted(self.matches, key=lambda m: m.match_date):
                if match.result:
                    if match.team1 == team:
                        opponent = match.team2
                        won = match.result.winner == team
                        score_diff = match.result.winner_score - match.result.loser_score if won else match.result.loser_score - match.result.winner_score
                    elif match.team2 == team:
                        opponent = match.team1
                        won = match.result.winner == team
                        score_diff = match.result.winner_score - match.result.loser_score if won else match.result.loser_score - match.result.winner_score
                    else:
                        continue

                    # Update head-to-head record
                    if won:
                        h2h_records[opponent.name]['wins'] += 1
                        wins += 1
                        if streak_type is None or streak_type is True:
                            current_streak += 1
                            streak_type = True
                        else:
                            current_streak = 1
                            streak_type = True
                    else:
                        h2h_records[opponent.name]['losses'] += 1
                        losses += 1
                        if streak_type is None or streak_type is False:
                            current_streak -= 1
                            streak_type = False
                        else:
                            current_streak = -1
                            streak_type = False
                    
                    game_diff += score_diff

            # Calculate win rate
            total_games = wins + losses
            win_rate = (wins / total_games * 100) if total_games > 0 else 0.0

            standings.append({
                'team': team,
                'matches_played': total_games,
                'wins': wins,
                'losses': losses,
                'win_rate': win_rate,
                'points': team.championship_points,
                'game_diff': game_diff,
                'h2h_records': h2h_records,
                'streak': current_streak
            })

        # Sort by: wins, h2h, game differential, win rate
        standings.sort(
            key=lambda x: (
                x['wins'],
                sum(record['wins'] for record in x['h2h_records'].values()),
                x['game_diff'],
                x['win_rate']
            ),
            reverse=True
        )

        return standings


class Season:
    def __init__(self, split: Split, year: int, start_date: datetime):
        self.split = split
        self.year = year
        self.start_date = start_date
        self.phase = SeasonPhase.OFF_SEASON
        self.current_week = 0
        self.playoff_teams: List[Team] = []
        self.champion: Optional[Team] = None

    @property
    def is_finished(self) -> bool:
        return self.phase == SeasonPhase.OFF_SEASON and self.champion is not None


class League:
    def __init__(self, name: str, divisions: Dict[str, List[Team]]):
        """Initialize league with divisions."""
        self.name = name
        self.divisions = {
            name: Division(name, teams)
            for name, teams in divisions.items()
        }
        self.current_season: Optional[Season] = None
        self.season_history: List[Season] = []
        
        # Validate minimum teams
        total_teams = sum(len(div.teams) for div in self.divisions.values())
        if total_teams < 4:
            raise ValueError("League must have at least 4 teams total")

    def get_all_teams(self) -> List[Team]:
        """Get all teams across all divisions."""
        return [
            team
            for division in self.divisions.values()
            for team in division.teams
        ]

    def generate_schedule(self, start_date: datetime) -> Dict[str, List[Match]]:
        """Generate schedule for each division."""
        division_schedules = {}
        
        for division_name, division in self.divisions.items():
            division.matches = []
            teams = division.teams
            num_teams = len(teams)
            
            # Each team plays every other team twice (home and away)
            num_rounds = 2
            matches_per_day = num_teams // 2
            days_per_week = 2  # Saturday and Sunday
            
            # Create list of all matchups
            all_matchups = []
            for round in range(num_rounds):
                for i, team1 in enumerate(teams):
                    for j, team2 in enumerate(teams[i + 1:], i + 1):
                        # Alternate home/away between rounds
                        if round % 2 == 0:
                            all_matchups.append((team1, team2))
                        else:
                            all_matchups.append((team2, team1))
            
            # Shuffle all matchups
            random.shuffle(all_matchups)
            
            # Organize into weeks
            current_date = start_date
            while all_matchups:
                # Saturday matches
                saturday_matches = []
                teams_playing_saturday = set()
                for _ in range(matches_per_day):
                    if not all_matchups:
                        break
                    # Find a valid matchup where neither team has played today
                    for i, (team1, team2) in enumerate(all_matchups):
                        if team1 not in teams_playing_saturday and team2 not in teams_playing_saturday:
                            saturday_matches.append(Match(team1, team2, current_date))
                            teams_playing_saturday.add(team1)
                            teams_playing_saturday.add(team2)
                            all_matchups.pop(i)
                            break
                
                # Sunday matches (next day)
                sunday_date = current_date + timedelta(days=1)
                sunday_matches = []
                teams_playing_sunday = set()
                for _ in range(matches_per_day):
                    if not all_matchups:
                        break
                    # Find a valid matchup where neither team has played today
                    for i, (team1, team2) in enumerate(all_matchups):
                        if team1 not in teams_playing_sunday and team2 not in teams_playing_sunday:
                            sunday_matches.append(Match(team1, team2, sunday_date))
                            teams_playing_sunday.add(team1)
                            teams_playing_sunday.add(team2)
                            all_matchups.pop(i)
                            break
                
                # Add matches to schedule
                division.matches.extend(saturday_matches)
                division.matches.extend(sunday_matches)
                
                # Move to next week
                current_date += timedelta(days=7)
            
            division_schedules[division_name] = division.matches
        
        return division_schedules

    def start_new_season(self, split: Split, start_date: datetime) -> None:
        """Start a new season."""
        # Archive current season if exists
        if self.current_season:
            self.season_history.append(self.current_season)
        
        # Create new season
        year = start_date.year
        self.current_season = Season(split, year, start_date)
        self.current_season.phase = SeasonPhase.REGULAR_SEASON
        
        # Generate schedules for all divisions
        self.generate_schedule(start_date)
        
        # Reset all team stats
        for team in self.get_all_teams():
            team.reset_stats()
        
    def get_matches_for_week(self, week: int) -> Dict[str, List[Match]]:
        """Get all matches for a specific week by division."""
        division_matches = {}
        
        for division_name, division in self.divisions.items():
            matches_per_week = len(division.teams) // 2 * 2  # 2 days per week
            start_idx = week * matches_per_week
            end_idx = start_idx + matches_per_week
            division_matches[division_name] = division.matches[start_idx:end_idx]
        
        return division_matches

    def simulate_week(self, player_team: Optional[Team] = None) -> Dict[str, List[MatchResult]]:
        """Simulate all matches for the current week across all divisions."""
        if not self.current_season or self.current_season.phase != SeasonPhase.REGULAR_SEASON:
            raise ValueError("Not in regular season")
        
        results = {}
        weekly_matches = self.get_matches_for_week(self.current_season.current_week)
        
        for division_name, matches in weekly_matches.items():
            division_results = []
            for match in matches:
                # Skip matches involving the player's team (if in this league)
                if player_team and (match.team1 == player_team or match.team2 == player_team):
                    continue
                    
                # Only simulate if match hasn't been played yet
                if not match.result:
                    match.result = match.simulate()
                    division_results.append(match.result)
            results[division_name] = division_results
        
        self.current_season.current_week += 1
        
        # Check if regular season is finished
        if self.is_regular_season_finished():
            self.start_playoffs()
        
        return results

    def is_regular_season_finished(self) -> bool:
        """Check if all regular season matches have been played."""
        regular_season_div = self.divisions.get("Regular Season")
        if not regular_season_div:
            return False
            
        return all(match.result is not None for match in regular_season_div.matches)

    def get_playoff_teams(self) -> List[Tuple[int, Team]]:
        """Get teams qualified for playoffs with their seeds."""
        # Get teams from regular season division
        regular_season_div = self.divisions.get("Regular Season")
        if not regular_season_div:
            return []
            
        # Get standings
        standings = regular_season_div.get_standings()
        
        # Take top 6 teams
        qualified_teams = []
        for i, team_stats in enumerate(standings[:6]):
            qualified_teams.append((i + 1, team_stats['team']))
        
        # Create playoffs division if it doesn't exist
        if "Playoffs" not in self.divisions:
            self.divisions["Playoffs"] = Division("Playoffs", [team for _, team in qualified_teams])
            
        # Set playoff teams in current season
        if self.current_season:
            self.current_season.playoff_teams = [team for _, team in qualified_teams]
        
        return qualified_teams

    def start_playoffs(self) -> None:
        """Initialize playoff bracket."""
        if not self.current_season:
            raise ValueError("No active season")
        
        # Get qualified teams with their seeds
        qualified_teams = self.get_playoff_teams()
        if len(qualified_teams) != 6:
            raise ValueError("Expected 6 playoff teams")
        
        # Ensure playoffs division exists
        if "Playoffs" not in self.divisions:
            self.divisions["Playoffs"] = Division("Playoffs", [team for _, team in qualified_teams])
        
        playoff_division = self.divisions["Playoffs"]
        playoff_division.matches.clear()  # Clear any existing matches
        
        # Create matches for each round
        # Quarter Finals (3rd vs 6th, 4th vs 5th)
        qf1 = Match(qualified_teams[2][1], qualified_teams[5][1], self.current_season.start_date + timedelta(days=7))
        qf2 = Match(qualified_teams[3][1], qualified_teams[4][1], self.current_season.start_date + timedelta(days=7))
        playoff_division.matches.extend([qf1, qf2])
        
        # Semi Finals (1st vs QF1 winner, 2nd vs QF2 winner)
        sf1 = Match(qualified_teams[0][1], None, self.current_season.start_date + timedelta(days=14))  # 1st seed vs QF1 winner
        sf2 = Match(qualified_teams[1][1], None, self.current_season.start_date + timedelta(days=14))  # 2nd seed vs QF2 winner
        playoff_division.matches.extend([sf1, sf2])
        
        # Finals
        finals = Match(None, None, self.current_season.start_date + timedelta(days=21))
        playoff_division.matches.append(finals)
        
        self.current_season.phase = SeasonPhase.PLAYOFFS
        self.current_season.playoff_teams = [team for _, team in qualified_teams]

    def simulate_playoff_match(self, match: Match) -> None:
        """Simulate a playoff match with special playoff rules."""
        # Playoff matches are best of 5
        match.simulate(best_of=5)
        
        # Award more points for playoff wins
        winner = match.result.winner
        loser = match.result.loser
        winner.championship_points += 50
        loser.championship_points += 20

    def simulate_playoff_round(self) -> bool:
        """Simulate current playoff round and return True if playoffs are complete."""
        if "Playoffs" not in self.divisions:
            return False
        
        playoff_division = self.divisions["Playoffs"]
        
        # First update the bracket to assign teams to matches
        next_round_matches = [m for m in playoff_division.matches if m.team1 is None or m.team2 is None]
        if next_round_matches:
            self.update_playoff_bracket()
        
        # Now simulate matches that have both teams assigned
        all_matches_complete = True
        for match in playoff_division.matches:
            if match.result is None:
                if match.team1 is not None and match.team2 is not None:
                    self.simulate_playoff_match(match)
                else:
                    all_matches_complete = False
        
        if all_matches_complete:
            # All matches are complete, check if we need to update bracket again
            next_round_matches = [m for m in playoff_division.matches if m.team1 is None or m.team2 is None]
            if next_round_matches:
                self.update_playoff_bracket()
                return False
            else:
                # No more matches to play, playoffs are done
                self.current_season.phase = SeasonPhase.OFF_SEASON
                finals_match = playoff_division.matches[-1]
                if finals_match.result:
                    self.current_season.champion = finals_match.result.winner
                return True
        
        return False

    def update_playoff_bracket(self) -> None:
        """Update the playoff bracket after matches are completed."""
        playoff_division = self.divisions.get("Playoffs")
        if not playoff_division:
            return
            
        matches = playoff_division.matches
        
        # Update semifinals (matches[2] and matches[3])
        # First QF winner goes to first SF (matches[2])
        if len(matches) > 2 and matches[0].result and matches[2].team2 is None:
            matches[2].team2 = matches[0].result.winner
        # Second QF winner goes to second SF (matches[3])
        if len(matches) > 3 and matches[1].result and matches[3].team2 is None:
            matches[3].team2 = matches[1].result.winner
            
        # Update finals (matches[4])
        # First SF winner goes to finals
        if len(matches) > 4 and matches[2].result and matches[4].team1 is None:
            matches[4].team1 = matches[2].result.winner
        # Second SF winner goes to finals
        if len(matches) > 4 and matches[3].result and matches[4].team2 is None:
            matches[4].team2 = matches[3].result.winner
            
        # Check if finals are complete and update champion
        if len(matches) > 4 and matches[4].result:
            self.current_season.champion = matches[4].result.winner

    def get_champion(self) -> Optional[Team]:
        """Get the champion of the league for the current season."""
        if not self.current_season:
            return None
            
        return self.current_season.champion

    def get_playoff_standings(self) -> List[Dict]:
        """Get current playoff standings and progress."""
        if not self.current_season or self.current_season.phase != SeasonPhase.PLAYOFFS:
            return []
            
        playoff_div = self.divisions.get("Playoffs")
        if not playoff_div:
            return []
            
        standings = []
        for team in self.current_season.playoff_teams:
            # Calculate playoff stats
            matches_played = [m for m in playoff_div.matches 
                            if m.result and (m.team1 == team or m.team2 == team)]
            wins = sum(1 for m in matches_played if m.result.winner == team)
            losses = sum(1 for m in matches_played if m.result.loser == team)
            
            # Get current round and opponent
            current_match = next((m for m in playoff_div.matches 
                                if not m.result and (m.team1 == team or m.team2 == team)), None)
            current_round = "Eliminated" if not current_match else self._get_playoff_round_name(current_match)
            opponent = current_match.team2 if current_match and current_match.team1 == team else \
                      current_match.team1 if current_match else None
            
            standings.append({
                'team': team,
                'wins': wins,
                'losses': losses,
                'current_round': current_round,
                'current_opponent': opponent,
                'championship_points': team.championship_points
            })
            
        return standings
        
    def _get_playoff_round_name(self, match: Match) -> str:
        """Get the name of the playoff round for a match."""
        playoff_div = self.divisions.get("Playoffs")
        if not playoff_div:
            return "Unknown"
            
        match_index = playoff_div.matches.index(match)
        total_matches = len(playoff_div.matches)
        
        if match_index == total_matches - 1:
            return "Finals"
        elif match_index >= total_matches - 3:
            return "Semi-Finals"
        else:
            return "Quarter-Finals"

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

    def get_tournament_stats(self) -> Dict:
        """Get comprehensive tournament statistics."""
        stats = {
            'name': self.name,
            'phase': self.current_phase,
            'start_date': self.start_date,
            'groups': {},
            'knockout_stage': []
        }
        
        # Group stage stats
        for group_name, teams in self.groups.items():
            group_stats = []
            for team in teams:
                matches = [m for m in self.group_stage_matches 
                          if m.result and (m.team1 == team or m.team2 == team)]
                wins = sum(1 for m in matches if m.result.winner == team)
                losses = sum(1 for m in matches if m.result.loser == team)
                
                group_stats.append({
                    'team': team,
                    'wins': wins,
                    'losses': losses,
                    'matches_played': len(matches),
                    'points': wins * 3  # 3 points per win
                })
            stats['groups'][group_name] = sorted(group_stats, 
                                               key=lambda x: (x['points'], x['wins']), 
                                               reverse=True)
        
        # Knockout stage stats
        if self.current_phase in ["Knockout Stage", "Finished"]:
            for match in self.knockout_matches:
                match_info = {
                    'team1': match.team1,
                    'team2': match.team2,
                    'completed': match.result is not None
                }
                if match.result:
                    match_info.update({
                        'winner': match.result.winner,
                        'loser': match.result.loser,
                        'score': f"{match.result.team1_score}-{match.result.team2_score}"
                    })
                stats['knockout_stage'].append(match_info)
        
        # Winner info
        if self.winner:
            stats['winner'] = self.winner
            
        return stats

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

    def simulate_all_leagues(self) -> Dict[str, Dict[str, List[MatchResult]]]:
        """Simulate matches for all leagues."""
        all_results = {}
        
        # Simulate player's league
        if self.league:
            all_results[self.league.name] = self.league.simulate_week(player_team=self.current_team)
            
        # Simulate other leagues
        for league_name, league in self.other_leagues.items():
            all_results[league_name] = league.simulate_week(player_team=None)  # No need to skip any matches
            
        return all_results
