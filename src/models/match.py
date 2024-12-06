from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import random

from .team import Team
from .player import Player, Role, PlayerStats
from .champion import Champion
from .draft import DraftState, DraftPick, DraftBan, DraftPhase, DraftPlayer

class ObjectiveType(Enum):
    TOWER = "Tower"
    DRAGON = "Dragon"
    BARON = "Baron"
    INHIBITOR = "Inhibitor"


class EventType(Enum):
    # Kill Events
    FIRST_BLOOD = "First Blood"
    SOLO_KILL = "Solo Kill"
    DOUBLE_KILL = "Double Kill"
    TRIPLE_KILL = "Triple Kill"
    QUADRA_KILL = "Quadra Kill"
    PENTA_KILL = "Penta Kill"
    
    # Team Fight Events
    TEAM_FIGHT_WIN = "Team Fight Victory"
    PERFECT_ACE = "Perfect Ace"
    COMEBACK_FIGHT = "Comeback Fight"
    BARON_FIGHT = "Baron Fight"
    DRAGON_FIGHT = "Dragon Fight"
    ELDER_EXECUTE = "Elder Execute"
    
    # Objective Events
    OBJECTIVE_STEAL = "Objective Steal"
    TOWER_DESTROYED = "Tower Destroyed"
    DRAGON_SECURED = "Dragon Secured"
    BARON_SECURED = "Baron Secured"
    INHIBITOR_DESTROYED = "Inhibitor Destroyed"
    
    # Skill Events
    OUTPLAY = "Outplay"
    JUNGLE_INVADE = "Jungle Invade"
    COUNTER_GANK = "Counter Gank"
    
    # Role-Specific Events
    TOP_SPLIT_PUSH = "Split Push Pressure"  # Top laner creates map pressure
    MID_ROAM = "Successful Roam"  # Mid laner roams to help other lanes
    ADC_KITING = "Perfect Kiting"  # ADC kites perfectly in a fight
    SUPPORT_VISION = "Vision Control"  # Support establishes vision control
    SUPPORT_SAVE = "Clutch Save"  # Support saves a teammate
    JUNGLE_OBJECTIVE = "Objective Control"  # Jungler secures multiple objectives


class DragonType(Enum):
    INFERNAL = "Infernal"
    OCEAN = "Ocean"
    MOUNTAIN = "Mountain"
    CLOUD = "Cloud"
    ELDER = "Elder"


@dataclass
class DragonState:
    infernal_stacks: int = 0
    ocean_stacks: int = 0
    mountain_stacks: int = 0
    cloud_stacks: int = 0
    has_elder: bool = False
    dragon_soul: Optional[DragonType] = None
    
    def add_dragon(self, dragon_type: DragonType) -> None:
        """Add a dragon stack and check for soul completion"""
        if dragon_type == DragonType.INFERNAL:
            self.infernal_stacks += 1
        elif dragon_type == DragonType.OCEAN:
            self.ocean_stacks += 1
        elif dragon_type == DragonType.MOUNTAIN:
            self.mountain_stacks += 1
        elif dragon_type == DragonType.CLOUD:
            self.cloud_stacks += 1
        elif dragon_type == DragonType.ELDER:
            self.has_elder = True
            
        # Check for dragon soul (4 dragons)
        total_dragons = (self.infernal_stacks + self.ocean_stacks + 
                        self.mountain_stacks + self.cloud_stacks)
        if total_dragons >= 4 and not self.dragon_soul:
            # Soul type is the dragon type with most stacks
            stacks = {
                DragonType.INFERNAL: self.infernal_stacks,
                DragonType.OCEAN: self.ocean_stacks,
                DragonType.MOUNTAIN: self.mountain_stacks,
                DragonType.CLOUD: self.cloud_stacks
            }
            self.dragon_soul = max(stacks.items(), key=lambda x: x[1])[0]
    
    def get_power_multiplier(self) -> float:
        """Calculate power multiplier based on dragon buffs"""
        multiplier = 1.0
        # Infernal gives damage boost
        multiplier += self.infernal_stacks * 0.04  # 4% per stack
        # Ocean gives sustain boost
        multiplier += self.ocean_stacks * 0.03     # 3% per stack
        # Mountain gives tankiness
        multiplier += self.mountain_stacks * 0.03  # 3% per stack
        # Cloud gives utility
        multiplier += self.cloud_stacks * 0.02     # 2% per stack
        
        # Soul and Elder provide significant boosts
        if self.dragon_soul:
            multiplier += 0.15  # 15% boost for having soul
        if self.has_elder:
            multiplier += 0.20  # 20% boost for elder buff
            
        return multiplier


@dataclass
class PlayerMatchStats:
    player: Player
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    cs: int = 0
    vision_score: int = 0
    damage_dealt: int = 0
    gold_earned: int = 0
    
    @property
    def kda(self) -> float:
        """Calculate KDA ratio."""
        if self.deaths == 0:
            return (self.kills + self.assists) * 1.0
        return round((self.kills + self.assists) / self.deaths, 2)


@dataclass
class TeamMatchStats:
    team: Team
    kills: int = 0
    deaths: int = 0
    towers: int = 0
    inhibitors: int = 0
    barons: int = 0
    dragons: int = 0
    total_gold: int = 0
    player_stats: Dict[Player, PlayerMatchStats] = field(default_factory=dict)
    dragon_state: DragonState = field(default_factory=DragonState)
    
    def __post_init__(self):
        """Initialize player stats for all players in the team."""
        if not self.team.players:
            raise ValueError(f"Team {self.team.name} has no players in roster")
        for player in self.team.players:
            self.player_stats[player] = PlayerMatchStats(player=player)


@dataclass
class TeamFightResult:
    """Represents the outcome of a team fight."""
    winner: Team
    loser: Team
    winner_kills: int
    loser_kills: int
    location: str
    objective_secured: Optional[str] = None
    mvp_player: Optional[Player] = None
    multi_kill: Optional[Tuple[Player, EventType]] = None

    @property
    def was_ace(self) -> bool:
        """Check if the fight was an ace (no deaths for winner)."""
        return self.loser_kills == 0

    @property
    def was_close(self) -> bool:
        """Check if the fight was close (within 2 kills)."""
        return abs(self.winner_kills - self.loser_kills) <= 2


@dataclass
class MatchEvent:
    type: EventType
    time: int  # Minutes into the game
    description: str
    player: Optional[Player] = None
    team: Optional[Team] = None
    fight_result: Optional[TeamFightResult] = None


@dataclass
class MatchResult:
    winner: Team
    loser: Team
    winner_score: int
    loser_score: int
    match_date: datetime
    duration: int  # Minutes
    winner_stats: TeamMatchStats
    loser_stats: TeamMatchStats
    events: List[MatchEvent]
    mvp: Player


class Match:
    def __init__(self, team1: Team, team2: Team, match_date: datetime):
        self.team1 = team1
        self.team2 = team2
        self.match_date = match_date
        self.result: Optional[MatchResult] = None
        self.draft_state: Optional[DraftState] = None
        
    def start_draft(self, team1_is_blue: bool = True) -> DraftState:
        """Initialize the draft phase of the match."""
        blue_team = self.team1 if team1_is_blue else self.team2
        red_team = self.team2 if team1_is_blue else self.team1
        self.draft_state = DraftState(blue_team=blue_team, red_team=red_team)
        return self.draft_state
        
    def auto_draft(self):
        """Auto-complete draft for non-player matches."""
        if not self.draft_state:
            self.start_draft()
            
        # Get available champions
        from src.data.champions import get_all_champions
        available_champions = list(get_all_champions().values())
        
        # Simulate draft picks for both teams
        for phase in range(10):  # 5 picks per team
            team = self.draft_state.blue_team if phase % 2 == 0 else self.draft_state.red_team
            
            # Pick a random champion that fits the role
            role = Role(list(Role)[phase % 5])  # Cycle through roles
            suitable_champions = [
                champ for champ in available_champions
                if role in champ.roles
            ]
            
            if suitable_champions:
                chosen_champion = random.choice(suitable_champions)
                available_champions.remove(chosen_champion)
                
                # Get the player for this role from the team's roster
                lineup = team.get_starting_lineup()
                player = lineup[role]
                if not player:  # If no player found for role, create a DraftPlayer
                    player = DraftPlayer(role=role)
                
                # Add pick to draft state
                self.draft_state.picks.append(DraftPick(
                    champion=chosen_champion,
                    team=team,
                    player=player,
                    pick_number=phase + 1
                ))
    
    def simulate(self, best_of: int = 1) -> MatchResult:
        """
        Simulate the match and return the result.
        
        Args:
            best_of (int): Number of games in the series (1, 3, or 5). Defaults to 1 for regular season.
        """
        if best_of not in [1, 3, 5]:
            raise ValueError("best_of must be 1, 3, or 5")
            
        # Auto-complete draft if not done
        if not self.draft_state or len(self.draft_state.picks) < 10:
            self.auto_draft()
            
        # Ensure draft has been completed
        if not self.draft_state or len(self.draft_state.picks) < 10:
            raise ValueError("Draft must be completed before simulating the match")
            
        games_to_win = (best_of + 1) // 2
        team1_wins = 0
        team2_wins = 0
        
        # Calculate team strengths (constant for the series)
        team1_strength = self.calculate_team_strength(self.team1)
        team2_strength = self.calculate_team_strength(self.team2)
        total_strength = team1_strength + team2_strength
        win_chance = team1_strength / total_strength
        
        # Simulate each game in the series
        while team1_wins < games_to_win and team2_wins < games_to_win:
            is_team1_winner = random.random() < win_chance
            if is_team1_winner:
                team1_wins += 1
            else:
                team2_wins += 1
                
        # Determine overall winner
        is_team1_winner = team1_wins > team2_wins
        winner = self.team1 if is_team1_winner else self.team2
        loser = self.team2 if is_team1_winner else self.team1
        winner_score = team1_wins if is_team1_winner else team2_wins
        loser_score = team2_wins if is_team1_winner else team1_wins
        
        # Get starting players (first player in each role)
        winner_players = {role: players[0] for role, players in winner.roster.items() if players}
        loser_players = {role: players[0] for role, players in loser.roster.items() if players}
        
        # Initialize match stats for both teams
        winner_stats = TeamMatchStats(team=winner)
        loser_stats = TeamMatchStats(team=loser)
        
        # Generate stats for winner's players (aggregate for the series)
        for role, player in winner_players.items():
            player_stats = self.generate_player_stats(
                player, 
                team1_strength if is_team1_winner else team2_strength,
                True
            )
            # Multiply stats by number of games
            player_stats.kills *= winner_score
            player_stats.deaths *= winner_score
            player_stats.assists *= winner_score
            player_stats.cs *= winner_score
            player_stats.vision_score *= winner_score
            player_stats.damage_dealt *= winner_score
            player_stats.gold_earned *= winner_score
            winner_stats.player_stats[player] = player_stats
            
        # Generate stats for loser's players (aggregate for the series)
        for role, player in loser_players.items():
            player_stats = self.generate_player_stats(
                player,
                team2_strength if is_team1_winner else team1_strength,
                False
            )
            # Multiply stats by number of games
            player_stats.kills *= loser_score
            player_stats.deaths *= loser_score
            player_stats.assists *= loser_score
            player_stats.cs *= loser_score
            player_stats.vision_score *= loser_score
            player_stats.damage_dealt *= loser_score
            player_stats.gold_earned *= loser_score
            loser_stats.player_stats[player] = player_stats
        
        # Calculate team-wide stats (aggregate for the series)
        winner_stats.kills = sum(stats.kills for stats in winner_stats.player_stats.values())
        winner_stats.deaths = sum(stats.deaths for stats in winner_stats.player_stats.values())
        winner_stats.assists = sum(stats.assists for stats in winner_stats.player_stats.values())
        winner_stats.total_gold = sum(stats.gold_earned for stats in winner_stats.player_stats.values())
        winner_stats.towers = random.randint(8, 11) * winner_score
        winner_stats.inhibitors = random.randint(2, 3) * winner_score
        winner_stats.barons = random.randint(1, 2) * winner_score
        winner_stats.dragons = random.randint(3, 4) * winner_score
        
        loser_stats.kills = sum(stats.kills for stats in loser_stats.player_stats.values())
        loser_stats.deaths = sum(stats.deaths for stats in loser_stats.player_stats.values())
        loser_stats.assists = sum(stats.assists for stats in loser_stats.player_stats.values())
        loser_stats.total_gold = sum(stats.gold_earned for stats in loser_stats.player_stats.values())
        loser_stats.towers = random.randint(2, 5) * loser_score
        loser_stats.inhibitors = random.randint(0, 2) * loser_score
        loser_stats.barons = random.randint(0, 1) * loser_score
        loser_stats.dragons = random.randint(0, 2) * loser_score
        
        # Create match result
        self.result = MatchResult(
            winner=winner,
            loser=loser,
            winner_score=winner_score,
            loser_score=loser_score,
            match_date=self.match_date,
            duration=random.randint(25, 45) * (winner_score + loser_score),  # Total duration of all games
            winner_stats=winner_stats,
            loser_stats=loser_stats,
            events=self.generate_match_events(winner, loser, winner_stats, loser_stats),
            mvp=self.select_mvp(winner_stats, loser_stats)
        )
        
        # Update team stats
        winner.update_stats_after_match(True, winner_score - loser_score)  # Game differential
        loser.update_stats_after_match(False, loser_score - winner_score)  # Game differential
        
        return self.result
    
    def calculate_player_performance(self, player: Union[Player, DraftPlayer], team_synergy: float) -> float:
        """Calculate a player's performance rating for this match."""
        # For DraftPlayer objects (non-player matches), return a random base rating
        if isinstance(player, DraftPlayer):
            return random.uniform(60, 80)  # Random rating between 60-80
            
        # For real players, use their stats
        base_rating = (
            player.stats.mechanical_skill * 0.35 +
            player.stats.game_knowledge * 0.35 +
            player.stats.communication * 0.15 +
            player.stats.leadership * 0.15
        )
        
        # Apply team synergy bonus
        synergy_bonus = team_synergy * 0.2
        
        # Random factor (-5 to +5)
        random_factor = random.uniform(-5, 5)
        
        return base_rating + synergy_bonus + random_factor
    
    def generate_player_stats(self, player: Player, team_strength: float, is_winner: bool) -> PlayerMatchStats:
        """Generate match statistics for a player."""
        # Base stats modified by team strength and win/loss
        base_modifier = 1.0 if is_winner else 0.7
        performance = team_strength * base_modifier
        
        # Generate stats based on performance
        return PlayerMatchStats(
            player=player,
            kills=random.randint(2 if is_winner else 0, 8 if is_winner else 4),
            deaths=random.randint(0 if is_winner else 2, 4 if is_winner else 6),
            assists=random.randint(4 if is_winner else 2, 12 if is_winner else 8),
            cs=random.randint(180 if is_winner else 150, 300 if is_winner else 250),
            vision_score=random.randint(20, 40),
            damage_dealt=random.randint(15000 if is_winner else 10000, 35000 if is_winner else 25000),
            gold_earned=random.randint(8000 if is_winner else 6000, 15000 if is_winner else 12000)
        )

    def _simulate_team_fight(self, winner: Team, loser: Team, location: str,
                           objective: Optional[str] = None, game_time: int = 0) -> TeamFightResult:
        """Simulate a team fight and generate detailed results."""
        # Determine number of kills (winner usually gets more)
        winner_kills = random.randint(2, 5)  # Winners get at least 2 kills
        loser_kills = random.randint(0, winner_kills - 1)  # Losers get fewer kills
        
        # Select MVP (more likely from winning team)
        mvp_candidates = winner.players + ([] if random.random() < 0.8 else loser.players)
        mvp_player = random.choice(mvp_candidates) if mvp_candidates else None
        
        # Check for multi-kills
        multi_kill = None
        if winner_kills >= 2:
            kill_types = {
                2: EventType.DOUBLE_KILL,
                3: EventType.TRIPLE_KILL,
                4: EventType.QUADRA_KILL,
                5: EventType.PENTA_KILL
            }
            if winner_kills in kill_types and random.random() < 0.7:
                multi_kill = (random.choice(winner.players), kill_types[winner_kills])
        
        return TeamFightResult(
            winner=winner,
            loser=loser,
            winner_kills=winner_kills,
            loser_kills=loser_kills,
            location=location,
            objective_secured=objective,
            mvp_player=mvp_player,
            multi_kill=multi_kill
        )

    def _generate_team_fight_description(self, fight_result: TeamFightResult, game_time: int) -> str:
        """Generate a detailed description of a team fight."""
        description = []
        
        # Basic fight outcome with team names
        if fight_result.was_ace and fight_result.winner_kills >= 3:
            description.append(f"{fight_result.winner.name} secured an ace against {fight_result.loser.name}")
        else:
            description.append(
                f"{fight_result.winner.name} won a {fight_result.winner_kills}-{fight_result.loser_kills} "
                f"fight against {fight_result.loser.name}"
            )
        
        # Location and objective context
        description.append(f"near {fight_result.location}")
        if fight_result.objective_secured:
            description.append(f"and secured {fight_result.objective_secured}")
        
        # Notable player performances
        if fight_result.mvp_player:
            if fight_result.was_ace:
                description.append(f"with {fight_result.mvp_player.name} leading the clean sweep")
            else:
                description.append(f"with {fight_result.mvp_player.name} making crucial plays")
        
        # Multi-kill achievements
        if fight_result.multi_kill:
            player, kill_type = fight_result.multi_kill
            if kill_type == EventType.PENTA_KILL:
                description.append(f"(PENTAKILL by {player.name}!)")
            else:
                description.append(f"({player.name} scored a {kill_type.value})")
        
        return " ".join(description)

    def generate_match_events(self, winner: Team, loser: Team, 
                            winner_stats: TeamMatchStats, loser_stats: TeamMatchStats) -> List[MatchEvent]:
        """Generate a list of significant events that occurred during the match."""
        events = []
        game_duration = random.randint(25, 45)  # Games last 25-45 minutes
        
        # Game locations for variety in descriptions
        locations = [
            "Baron pit", "Dragon pit", "top river", "bottom river",
            "top jungle", "bottom jungle", "mid lane", "top lane", "bottom lane",
            "enemy blue buff", "enemy red buff"
        ]
        
        # First blood (happens between 2-10 minutes)
        first_blood_time = random.randint(2, 10)
        first_blood_team = winner if random.random() < 0.7 else loser
        first_blood_player = random.choice(list(first_blood_team.players))
        events.append(MatchEvent(
            type=EventType.FIRST_BLOOD,
            time=first_blood_time,
            description=f"{first_blood_player.name} ({first_blood_team.name}) drew first blood!",
            player=first_blood_player,
            team=first_blood_team
        ))
        
        # Track game state for comeback mechanics
        current_winner = winner
        current_loser = loser
        current_winner_score = 0
        current_loser_score = 0
        
        # Generate major events throughout the game
        num_events = random.randint(8, 15)
        last_event_time = first_blood_time
        
        for _ in range(num_events):
            # Ensure events are spread out
            min_time = last_event_time + 1
            max_time = min(last_event_time + 8, game_duration - 5)
            
            # If min_time is greater than max_time, adjust max_time
            if min_time > max_time:
                max_time = min_time
            
            # Generate the event time
            time = min_time if min_time >= max_time else random.randint(min_time, max_time)
            last_event_time = time
            
            # Determine event type based on game state
            if random.random() < 0.4:  # 40% chance of team fight
                location = random.choice(locations)
                objective = None
                
                # Determine if fight is over an objective
                if random.random() < 0.6:  # 60% chance fight is over objective
                    if time > 20 and random.random() < 0.3:
                        objective = "Baron Nashor"
                    else:
                        dragon_type = random.choice(list(DragonType))
                        objective = f"{dragon_type.value} Dragon"
                
                # Comeback mechanics: losing team has a better chance in later game
                comeback_chance = 0.3 + (time / game_duration * 0.2)  # Increases from 0.3 to 0.5
                fight_winner = current_loser if random.random() < comeback_chance else current_winner
                fight_loser = current_winner if fight_winner == current_loser else current_loser
                
                # Simulate team fight
                fight_result = self._simulate_team_fight(
                    fight_winner, fight_loser, location, objective, time
                )
                
                # Update game state
                if fight_winner == current_winner:
                    current_winner_score += fight_result.winner_kills
                else:
                    current_loser_score += fight_result.winner_kills
                    # Check for momentum shift
                    if current_loser_score > current_winner_score:
                        current_winner, current_loser = current_loser, current_winner
                        current_winner_score, current_loser_score = current_loser_score, current_winner_score
                
                # Create event
                event_type = (
                    EventType.COMEBACK_FIGHT if fight_winner == loser
                    else EventType.PERFECT_ACE if fight_result.was_ace
                    else EventType.TEAM_FIGHT_WIN
                )
                
                events.append(MatchEvent(
                    type=event_type,
                    time=time,
                    description=self._generate_team_fight_description(fight_result, time),
                    team=fight_winner,
                    fight_result=fight_result
                ))
                
            else:  # Individual plays and objectives
                event_type = random.choice([
                    EventType.SOLO_KILL,
                    EventType.OBJECTIVE_STEAL,
                    EventType.TOWER_DESTROYED,
                    EventType.DRAGON_SECURED,
                    EventType.BARON_SECURED,
                    EventType.INHIBITOR_DESTROYED,
                    EventType.OUTPLAY,
                    EventType.JUNGLE_INVADE,
                    EventType.COUNTER_GANK,
                    EventType.TOP_SPLIT_PUSH,
                    EventType.MID_ROAM
                ])
                
                # Comeback mechanics for individual events too
                comeback_chance = 0.3 + (time / game_duration * 0.2)
                team = current_loser if random.random() < comeback_chance else current_winner
                player = random.choice(list(team.players))
                
                events.append(MatchEvent(
                    type=event_type,
                    time=time,
                    description=self._generate_event_description(event_type, player, team),
                    player=player,
                    team=team
                ))
        
        return events
    
    def _generate_event_description(self, event_type: EventType, player: Player, team: Team) -> str:
        """Generate a descriptive message for a match event."""
        if event_type == EventType.SOLO_KILL:
            actions = [
                f"{player.name} outplayed their opponent for a clean solo kill in {player.role.value}",
                f"{player.name} secured a spectacular solo kill in the {player.role.value} lane",
                f"Incredible mechanics by {player.name} to get a solo kill in {player.role.value}"
            ]
            return random.choice(actions)
            
        elif event_type == EventType.OBJECTIVE_STEAL:
            if random.random() < 0.3:  # Epic monster steal
                objective = random.choice(["Baron", "Elder Dragon"])
                return f"INCREDIBLE! {player.name} steals {objective} for {team.name}!"
            else:
                objective = random.choice(["Dragon", "Rift Herald"])
                return f"Amazing {objective} steal by {player.name} for {team.name}"
            
        elif event_type == EventType.TOWER_DESTROYED:
            locations = ["outer", "inner", "inhibitor"]
            lanes = ["top", "mid", "bottom"]
            tower = f"{random.choice(locations)} {random.choice(lanes)} tower"
            return f"{team.name} takes down the {tower}"
            
        elif event_type == EventType.DRAGON_SECURED:
            dragon_type = random.choice(list(DragonType))
            if dragon_type == DragonType.ELDER:
                return f"{team.name} secures the Elder Dragon! {player.name} gets the finishing blow"
            return f"{team.name} claims the {dragon_type.value} Dragon with {player.name} securing the objective"
            
        elif event_type == EventType.BARON_SECURED:
            minutes = random.randint(20, 35)
            return f"{minutes} min Baron secured by {team.name}, {player.name} dealt the final damage"
            
        elif event_type == EventType.INHIBITOR_DESTROYED:
            lanes = ["top", "mid", "bottom"]
            lane = random.choice(lanes)
            return f"{team.name} breaks the {lane} inhibitor, opening up the base"
            
        elif event_type == EventType.OUTPLAY:
            scenarios = [
                f"{player.name} pulls off an incredible 1v2 outplay in {player.role.value}",
                f"Mechanical masterclass by {player.name} to turn around a gank",
                f"{player.name} shows off their skills with a beautiful outplay"
            ]
            return random.choice(scenarios)
            
        elif event_type == EventType.JUNGLE_INVADE:
            if player.role == Role.JUNGLE:
                return f"{player.name} successfully invades the enemy jungle, denying crucial resources"
            else:
                return f"{team.name} invades the enemy jungle with {player.name} leading the charge"
            
        elif event_type == EventType.COUNTER_GANK:
            if player.role == Role.JUNGLE:
                return f"Perfect counter gank by {player.name} to turn the tide"
            else:
                return f"{player.name} helps turn around a gank in {player.role.value}"
            
        elif event_type == EventType.TOP_SPLIT_PUSH:
            return f"{player.name} creates pressure with a successful split push in top lane"
            
        elif event_type == EventType.MID_ROAM:
            return f"{player.name} roams effectively to help out other lanes"
            
        elif event_type == EventType.ADC_KITING:
            return f"{player.name} kites perfectly in a team fight, avoiding damage"
            
        elif event_type == EventType.SUPPORT_VISION:
            return f"{player.name} establishes vision control, helping their team"
            
        elif event_type == EventType.SUPPORT_SAVE:
            return f"{player.name} makes a clutch save, turning around a team fight"
            
        elif event_type == EventType.JUNGLE_OBJECTIVE:
            return f"{player.name} secures multiple objectives, giving their team an advantage"
            
        return f"{player.name} makes a great play for {team.name}"
    
    def select_mvp(self, winner_stats: TeamMatchStats, loser_stats: TeamMatchStats) -> Player:
        """Select the MVP of the match based on performance statistics."""
        all_players = list(winner_stats.player_stats.items()) + list(loser_stats.player_stats.items())
        
        def calculate_mvp_score(player_tuple) -> float:
            player, stats = player_tuple
            # Calculate MVP score based on KDA, damage, and vision
            kda_score = stats.kda * 10
            damage_score = stats.damage_dealt / 1000
            vision_score = stats.vision_score / 2
            return kda_score + damage_score + vision_score
        
        # Return the player with highest MVP score
        mvp_player, _ = max(all_players, key=calculate_mvp_score)
        return mvp_player
    
    def calculate_team_strength(self, team: Team) -> float:
        """Calculate overall team strength based on players and composition."""
        # Get team's champions from draft
        team_picks = [pick for pick in self.draft_state.picks if pick.team == team]
        if not team_picks:
            return 0.0
            
        # Base strength from player skills
        base_strength = sum(self.calculate_player_performance(pick.player, 0) for pick in team_picks) / 5
        
        # Calculate composition score (0-100)
        comp_score = self._analyze_team_composition(team_picks)
        
        # Final strength is weighted average of base strength and composition
        return (base_strength * 0.7) + (comp_score * 0.3)

    def _analyze_team_composition(self, team_picks: List[DraftPick]) -> float:
        """Analyze team composition strength (returns 0-100)."""
        score = 0
        champions = [pick.champion for pick in team_picks]
        
        # 1. Damage Balance (25 points)
        damage_types = self._count_damage_types(champions)
        if damage_types['physical'] >= 2 and damage_types['magic'] >= 2:
            score += 25  # Balanced damage
        elif damage_types['physical'] >= 1 and damage_types['magic'] >= 1:
            score += 15  # Somewhat balanced
        else:
            score += 5   # Too one-dimensional
            
        # 2. Team Fight Potential (25 points)
        cc_score = self._evaluate_cc(champions)
        engage_score = self._evaluate_engage(champions)
        score += (cc_score + engage_score) / 2
        
        # 3. Win Condition Diversity (25 points)
        win_conditions = self._analyze_win_conditions(champions)
        score += win_conditions
        
        # 4. Power Curve Balance (25 points)
        power_curve = self._analyze_power_curve(champions)
        score += power_curve
        
        return score

    def _count_damage_types(self, champions: List[Champion]) -> Dict[str, int]:
        """Count physical and magic damage dealers."""
        damage_types = {'physical': 0, 'magic': 0}
        
        # Define primary damage type for each champion
        physical_damage = ['Ashe', 'Caitlyn', 'Jinx', 'Lucian', 'Tristana', 'Zed', 'Yasuo', 'Yone', 'Talon']
        magic_damage = ['Ahri', 'Annie', 'Brand', 'Lux', 'Syndra', 'Viktor', 'Veigar', 'Kassadin']
        
        for champion in champions:
            if champion.name in physical_damage:
                damage_types['physical'] += 1
            elif champion.name in magic_damage:
                damage_types['magic'] += 1
            # Some champions can be both or neither
            
        return damage_types

    def _evaluate_cc(self, champions: List[Champion]) -> float:
        """Evaluate crowd control potential (0-12.5 points)."""
        score = 0
        high_cc = ['Leona', 'Nautilus', 'Thresh', 'Morgana', 'Lux', 'Malphite']
        medium_cc = ['Ahri', 'Annie', 'Ashe', 'Jhin', 'Sett']
        
        for champion in champions:
            if champion.name in high_cc:
                score += 2.5
            elif champion.name in medium_cc:
                score += 1.5
                
        return min(12.5, score)  # Cap at 12.5 points

    def _evaluate_engage(self, champions: List[Champion]) -> float:
        """Evaluate engage potential (0-12.5 points)."""
        score = 0
        strong_engage = ['Malphite', 'Leona', 'Nautilus', 'Hecarim', 'Sejuani']
        medium_engage = ['Thresh', 'Rakan', 'Sett', 'Gragas']
        
        for champion in champions:
            if champion.name in strong_engage:
                score += 2.5
            elif champion.name in medium_engage:
                score += 1.5
                
        return min(12.5, score)  # Cap at 12.5 points

    def _analyze_win_conditions(self, champions: List[Champion]) -> float:
        """Analyze diversity of win conditions (0-25 points)."""
        score = 0
        
        # Check for different win conditions
        conditions = {
            'teamfight': self._has_teamfight_comp(champions),
            'pick': self._has_pick_comp(champions),
            'split_push': self._has_split_push(champions),
            'poke': self._has_poke_comp(champions),
            'scaling': self._has_scaling_comp(champions)
        }
        
        # Score based on number of viable win conditions
        viable_conditions = sum(1 for x in conditions.values() if x)
        score = min(25, viable_conditions * 8)
        
        return score

    def _has_teamfight_comp(self, champions: List[Champion]) -> bool:
        """Check if team has strong teamfight composition."""
        teamfight_champs = ['Malphite', 'Orianna', 'Miss Fortune', 'Leona', 'Amumu']
        return any(c.name in teamfight_champs for c in champions)

    def _has_pick_comp(self, champions: List[Champion]) -> bool:
        """Check if team has strong pick composition."""
        pick_champs = ['Thresh', 'Blitzcrank', 'Ahri', 'Pyke', 'Morgana']
        return any(c.name in pick_champs for c in champions)

    def _has_split_push(self, champions: List[Champion]) -> bool:
        """Check if team has strong split push potential."""
        split_push_champs = ['Fiora', 'Jax', 'Tryndamere', 'Yorick', 'Nasus']
        return any(c.name in split_push_champs for c in champions)

    def _has_poke_comp(self, champions: List[Champion]) -> bool:
        """Check if team has strong poke composition."""
        poke_champs = ['Ziggs', 'Xerath', 'Jayce', 'Nidalee', 'Varus']
        return any(c.name in poke_champs for c in champions)

    def _has_scaling_comp(self, champions: List[Champion]) -> bool:
        """Check if team has strong late game scaling."""
        scaling_champs = ['Kayle', 'Kassadin', 'Vayne', 'Veigar', 'Vladimir']
        return any(c.name in scaling_champs for c in champions)

    def _analyze_power_curve(self, champions: List[Champion]) -> float:
        """Analyze team's power curve balance (0-25 points)."""
        early_game = 0
        mid_game = 0
        late_game = 0
        
        for champion in champions:
            if champion.name in ['Lee Sin', 'Pantheon', 'Draven', 'Renekton']:
                early_game += 1
            elif champion.name in ['Orianna', 'Viktor', 'Syndra', 'Riven']:
                mid_game += 1
            elif champion.name in ['Kayle', 'Kassadin', 'Vayne', 'Vladimir']:
                late_game += 1
                
        # Score based on power curve distribution
        if early_game and mid_game and late_game:
            return 25  # Perfect balance
        elif (early_game and mid_game) or (mid_game and late_game):
            return 20  # Good balance
        elif early_game >= 3 or mid_game >= 3 or late_game >= 3:
            return 15  # Strong in one phase
        else:
            return 10  # Unclear power curve

    def __str__(self) -> str:
        if self.result is None:
            return f"{self.team1.name} vs {self.team2.name} - {self.match_date}"
        
        return (
            f"{self.result.winner.name} defeated {self.result.loser.name} "
            f"{self.result.winner_score}-{self.result.loser_score}"
        )
