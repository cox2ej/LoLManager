from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
                                QGroupBox, QScrollArea, QSpacerItem, QSizePolicy, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
import random
from typing import List, Dict

from src.models.match import Match, MatchResult, MatchEvent, EventType, TeamMatchStats, DragonType, DragonState
from src.models.player import Player, Role
from src.models.team import Team
from datetime import datetime


class MatchSimulationScreen(QWidget):
    match_completed = pyqtSignal(Match)  # Signal emitted when match is done
    
    def __init__(self, main_window, match: Match):
        super().__init__()
        self.main_window = main_window
        self.match = match
        self.current_time = 0  # Current game time in minutes
        self.events = []  # List to store match events
        self.winner_stats = None
        self.loser_stats = None
        
        # Initialize dictionaries for team and player stats
        self.team_stats = {}  # Will store team stats labels
        self.player_stats = {}  # Will store player stats labels
        
        self.init_ui()
        self.start_simulation()
        
    def init_ui(self):
        """Initialize the match simulation UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Match header
        header_layout = self.create_header()
        layout.addLayout(header_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left side - Team 1 stats
        team1_stats = self.create_team_stats_panel(self.match.team1)
        content_layout.addWidget(team1_stats)
        
        # Center - Match events feed
        events_panel = self.create_events_panel()
        content_layout.addWidget(events_panel, stretch=2)
        
        # Right side - Team 2 stats
        team2_stats = self.create_team_stats_panel(self.match.team2)
        content_layout.addWidget(team2_stats)
        
        layout.addLayout(content_layout)
        
        # Game timer and progress
        timer_layout = self.create_timer_panel()
        layout.addLayout(timer_layout)
        
        self.setLayout(layout)
        
    def create_header(self) -> QHBoxLayout:
        """Create the match header with team names and current score."""
        layout = QHBoxLayout()
        
        # Team 1 score
        self.team1_score_label = QLabel("0")
        self.team1_score_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        self.team1_score_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Team 1 name
        team1_name = QLabel(self.match.team1.name)
        team1_name.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        team1_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # VS label
        vs_label = QLabel("VS")
        vs_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vs_label.setStyleSheet("color: #FF4444;")
        
        # Team 2 name
        team2_name = QLabel(self.match.team2.name)
        team2_name.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        team2_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Team 2 score
        self.team2_score_label = QLabel("0")
        self.team2_score_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        self.team2_score_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Add to layout with proper spacing
        team1_layout = QVBoxLayout()
        team1_layout.addWidget(team1_name)
        team1_layout.addWidget(self.team1_score_label)
        
        team2_layout = QVBoxLayout()
        team2_layout.addWidget(team2_name)
        team2_layout.addWidget(self.team2_score_label)
        
        layout.addLayout(team1_layout)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        layout.addWidget(vs_label)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        layout.addLayout(team2_layout)
        
        return layout
        
    def create_team_stats_panel(self, team):
        """Create a panel showing team statistics."""
        panel = QGroupBox(team.name)
        panel.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QGridLayout()
        
        # Initialize stats dictionary for this team
        self.team_stats[team] = {
            "kills": QLabel("0"),
            "deaths": QLabel("0"),
            "towers": QLabel("0"),
            "dragons": QLabel("0"),
            "barons": QLabel("0"),
            "gold": QLabel("0"),
            "dragon_state": DragonState()
        }
        
        # Team objectives
        objectives_group = QGroupBox("Objectives")
        objectives_layout = QGridLayout()
        
        # Add stats labels with appropriate styling
        stats = [
            ("Kills", self.team_stats[team]["kills"]),
            ("Deaths", self.team_stats[team]["deaths"]),
            ("Towers", self.team_stats[team]["towers"]),
            ("Dragons", self.team_stats[team]["dragons"]),
            ("Barons", self.team_stats[team]["barons"]),
            ("Gold", self.team_stats[team]["gold"])
        ]
        
        for i, (label, value_label) in enumerate(stats):
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            value_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            objectives_layout.addWidget(label_widget, i, 0)
            objectives_layout.addWidget(value_label, i, 1)
            
        objectives_group.setLayout(objectives_layout)
        layout.addWidget(objectives_group)
        
        # Player performances
        players_group = QGroupBox("Players")
        players_layout = QVBoxLayout()
        
        # Initialize player stats dictionary for this team if not already done
        if team not in self.player_stats:
            self.player_stats[team] = {}
        
        # Iterate through roles and get the starting player (first in list)
        for role in Role:
            if role in team.roster and team.roster[role]:  # Check if role exists and has players
                player = team.roster[role][0]  # Get the starting player
                
                player_frame = QFrame()
                player_layout = QGridLayout()
                
                # Player name and role
                name_label = QLabel(f"{player.name} ({role.value})")
                name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                player_layout.addWidget(name_label, 0, 0, 1, 2)
                
                # Stats labels
                kda_label = QLabel("KDA: 0/0/0")
                cs_label = QLabel("CS: 0")
                gold_label = QLabel("Gold: 0")
                
                player_layout.addWidget(kda_label, 1, 0)
                player_layout.addWidget(cs_label, 1, 1)
                player_layout.addWidget(gold_label, 2, 0, 1, 2)
                
                self.player_stats[team][player] = {
                    "kda": kda_label,
                    "cs": cs_label,
                    "gold": gold_label
                }
                
                player_frame.setLayout(player_layout)
                players_layout.addWidget(player_frame)
            
        players_group.setLayout(players_layout)
        layout.addWidget(players_group)
        
        panel.setLayout(layout)
        return panel
        
    def create_events_panel(self) -> QGroupBox:
        """Create the match events feed panel."""
        group = QGroupBox("Match Events")
        layout = QVBoxLayout()
        
        # Create scrollable area for events
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Container for events
        self.events_container = QWidget()
        self.events_layout = QVBoxLayout()
        self.events_layout.addStretch()
        self.events_container.setLayout(self.events_layout)
        
        scroll.setWidget(self.events_container)
        layout.addWidget(scroll)
        
        group.setLayout(layout)
        return group
        
    def create_timer_panel(self) -> QHBoxLayout:
        """Create the game timer and progress panel."""
        layout = QHBoxLayout()
        
        # Game time label
        self.time_label = QLabel("0:00")
        self.time_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        # Game progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(45)  # Typical game length
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
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
        
        layout.addWidget(self.time_label)
        layout.addWidget(self.progress_bar, stretch=1)
        
        return layout
        
    def add_event(self, event: MatchEvent):
        """Add a new event to the events feed."""
        event_frame = QFrame()
        event_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
        """)
        
        event_layout = QVBoxLayout()
        
        # Event time and type
        header_layout = QHBoxLayout()
        time_label = QLabel(f"{event.time}:00")
        time_label.setStyleSheet("color: #888888;")
        header_layout.addWidget(time_label)
        
        type_label = QLabel(event.type.value)
        type_label.setStyleSheet("color: #FF4444; font-weight: bold;")
        header_layout.addWidget(type_label)
        header_layout.addStretch()
        
        # Event description
        desc_label = QLabel(event.description)
        desc_label.setWordWrap(True)
        
        event_layout.addLayout(header_layout)
        event_layout.addWidget(desc_label)
        
        event_frame.setLayout(event_layout)
        
        # Add new event at the top
        self.events_layout.insertWidget(0, event_frame)
        
    def update_stats(self, winner_stats: TeamMatchStats, loser_stats: TeamMatchStats):
        """Update team and player statistics."""
        self.winner_stats = winner_stats
        self.loser_stats = loser_stats
        
        # Update team stats
        for team, stats in [(self.match.team1, winner_stats if winner_stats.team == self.match.team1 else loser_stats),
                          (self.match.team2, winner_stats if winner_stats.team == self.match.team2 else loser_stats)]:
            # Update team stats
            self.team_stats[team]["kills"].setText(str(stats.kills))
            self.team_stats[team]["deaths"].setText(str(stats.deaths))
            self.team_stats[team]["towers"].setText(str(stats.towers))
            self.team_stats[team]["dragons"].setText(str(stats.dragons))
            self.team_stats[team]["barons"].setText(str(stats.barons))
            self.team_stats[team]["gold"].setText(f"{stats.total_gold:,}")
            
            # Update player stats
            for role, players in team.roster.items():
                if players:  # If there are players in this role
                    player = players[0]  # Get starting player
                    if player in stats.player_stats:
                        player_stats = stats.player_stats[player]
                        if player in self.player_stats[team]:
                            # Update KDA
                            kda = f"{player_stats.kills}/{player_stats.deaths}/{player_stats.assists}"
                            self.player_stats[team][player]["kda"].setText(f"KDA: {kda}")
                            
                            # Update CS
                            self.player_stats[team][player]["cs"].setText(f"CS: {player_stats.cs}")
                            
                            # Update Gold
                            self.player_stats[team][player]["gold"].setText(f"Gold: {player_stats.gold_earned:,}")
        
    def update_score(self, team1_score: int, team2_score: int):
        """Update the match score."""
        self.team1_score_label.setText(str(team1_score))
        self.team2_score_label.setText(str(team2_score))
        
    def start_simulation(self):
        """Start the match simulation."""
        # Initialize empty stats for both teams
        self.winner_stats = TeamMatchStats(team=self.match.team1)
        self.loser_stats = TeamMatchStats(team=self.match.team2)
        
        # Set up game duration (25-45 minutes)
        self.game_duration = random.randint(25, 45)
        self.progress_bar.setMaximum(self.game_duration)
        
        # Generate events spread across the game duration
        self.events = self.generate_match_events()
        self.next_event_index = 0
        
        # Initialize stats display
        self.update_stats(self.winner_stats, self.loser_stats)
        
        # Set up timers
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.update_game_time)
        self.game_timer.start(250)  # Update every 250ms for smooth progress
        
        # For CS tracking
        self.last_cs_update = 0
        
    def generate_match_events(self) -> List[MatchEvent]:
        """Generate a list of match events spread across the game duration."""
        events = []
        
        # Determine winner (60% chance for team1 to win)
        self.match.result = MatchResult(
            winner=self.match.team1 if random.random() < 0.6 else self.match.team2,
            loser=self.match.team2 if self.match.team1.name == self.winner_stats.team.name else self.match.team1,
            winner_score=1,
            loser_score=0,
            match_date=self.match.match_date,
            duration=self.game_duration,
            winner_stats=self.winner_stats,
            loser_stats=self.loser_stats,
            events=events,
            mvp=None  # Will be set at the end
        )
        
        # Track available dragons for spawning
        available_dragons = [
            DragonType.INFERNAL,
            DragonType.OCEAN,
            DragonType.MOUNTAIN,
            DragonType.CLOUD
        ]
        next_dragon_type = random.choice(available_dragons)  # First dragon type
        next_dragon_time = 5  # First dragon spawns at 5 minutes
        
        # Early game events (0-15 minutes)
        for minute in range(0, 15, 2):  # Every 2 minutes instead of 3
            if random.random() < 0.8:  # 80% chance instead of 70%
                if random.random() < 0.5:  # Equal chance for both teams early
                    team_stats = self.winner_stats
                else:
                    team_stats = self.loser_stats
                
                event_time = minute + random.randint(-1, 1)
                player = random.choice(list(team_stats.player_stats.keys()))
                
                # Role-specific early game events
                if player.role == Role.JUNGLE:
                    event_type = random.choice([
                        EventType.JUNGLE_INVADE,
                        EventType.COUNTER_GANK,
                        EventType.JUNGLE_OBJECTIVE
                    ])
                elif player.role == Role.MID:
                    event_type = random.choice([
                        EventType.MID_ROAM,
                        EventType.SOLO_KILL,
                        EventType.OUTPLAY
                    ])
                elif player.role == Role.TOP:
                    event_type = random.choice([
                        EventType.TOP_SPLIT_PUSH,
                        EventType.SOLO_KILL,
                        EventType.TOWER_DESTROYED
                    ])
                elif player.role == Role.ADC:
                    event_type = random.choice([
                        EventType.ADC_KITING,
                        EventType.SOLO_KILL,
                        EventType.TOWER_DESTROYED
                    ])
                else:  # SUPPORT
                    event_type = random.choice([
                        EventType.SUPPORT_VISION,
                        EventType.SUPPORT_SAVE,
                        EventType.COUNTER_GANK
                    ])
                
                events.append(MatchEvent(
                    type=event_type,
                    time=event_time,
                    description=self._generate_event_description(event_type, player, team_stats.team),
                    player=player,
                    team=team_stats.team
                ))
                
                # Chance for follow-up event
                if random.random() < 0.3:  # 30% chance for follow-up
                    follow_up_time = event_time + random.randint(0, 1)
                    follow_up_player = random.choice(list(team_stats.player_stats.keys()))
                    
                    if event_type in [EventType.JUNGLE_INVADE, EventType.COUNTER_GANK]:
                        follow_up_type = random.choice([EventType.SOLO_KILL, EventType.OBJECTIVE_STEAL])
                    elif event_type == EventType.MID_ROAM:
                        follow_up_type = random.choice([EventType.TOWER_DESTROYED, EventType.DRAGON_SECURED])
                    elif event_type == EventType.TOP_SPLIT_PUSH:
                        follow_up_type = EventType.TOWER_DESTROYED
                    else:
                        follow_up_type = random.choice([EventType.OUTPLAY, EventType.TEAM_FIGHT_WIN])
                    
                    events.append(MatchEvent(
                        type=follow_up_type,
                        time=follow_up_time,
                        description=self._generate_event_description(follow_up_type, follow_up_player, team_stats.team),
                        player=follow_up_player,
                        team=team_stats.team
                    ))
        
        # Mid game events (15-25 minutes)
        for minute in range(15, 26, 2):  # Every 2 minutes instead of 3
            if random.random() < 0.85:  # 85% chance instead of 70%
                if random.random() < 0.6:  # 60% chance for winning team
                    team_stats = self.winner_stats
                else:
                    team_stats = self.loser_stats
                
                event_time = minute + random.randint(-1, 1)
                player = random.choice(list(team_stats.player_stats.keys()))
                
                # Role-specific mid game events
                if player.role == Role.JUNGLE:
                    event_type = random.choice([
                        EventType.JUNGLE_OBJECTIVE,
                        EventType.OBJECTIVE_STEAL,
                        EventType.DRAGON_SECURED,
                        EventType.BARON_SECURED
                    ])
                elif player.role == Role.MID:
                    event_type = random.choice([
                        EventType.MID_ROAM,
                        EventType.TEAM_FIGHT_WIN,
                        EventType.OUTPLAY,
                        EventType.TOWER_DESTROYED
                    ])
                elif player.role == Role.TOP:
                    event_type = random.choice([
                        EventType.TOP_SPLIT_PUSH,
                        EventType.INHIBITOR_DESTROYED,
                        EventType.TEAM_FIGHT_WIN
                    ])
                elif player.role == Role.ADC:
                    event_type = random.choice([
                        EventType.ADC_KITING,
                        EventType.TEAM_FIGHT_WIN,
                        EventType.TOWER_DESTROYED
                    ])
                else:  # SUPPORT
                    event_type = random.choice([
                        EventType.SUPPORT_VISION,
                        EventType.SUPPORT_SAVE,
                        EventType.TEAM_FIGHT_WIN
                    ])
                
                events.append(MatchEvent(
                    type=event_type,
                    time=event_time,
                    description=self._generate_event_description(event_type, player, team_stats.team),
                    player=player,
                    team=team_stats.team
                ))
                
                # Higher chance for follow-up event in mid game
                if random.random() < 0.4:  # 40% chance for follow-up
                    follow_up_time = event_time + random.randint(0, 1)
                    follow_up_player = random.choice(list(team_stats.player_stats.keys()))
                    
                    if event_type in [EventType.DRAGON_SECURED, EventType.BARON_SECURED]:
                        follow_up_type = EventType.TEAM_FIGHT_WIN
                    elif event_type == EventType.TEAM_FIGHT_WIN:
                        follow_up_type = random.choice([
                            EventType.TOWER_DESTROYED,
                            EventType.INHIBITOR_DESTROYED,
                            EventType.DRAGON_SECURED
                        ])
                    else:
                        follow_up_type = random.choice([
                            EventType.OBJECTIVE_STEAL,
                            EventType.OUTPLAY,
                            EventType.TEAM_FIGHT_WIN
                        ])
                    
                    events.append(MatchEvent(
                        type=follow_up_type,
                        time=follow_up_time,
                        description=self._generate_event_description(follow_up_type, follow_up_player, team_stats.team),
                        player=follow_up_player,
                        team=team_stats.team
                    ))
        
        # Late game events (25+ minutes)
        for minute in range(25, self.game_duration - 5, 2):  # Every 2 minutes instead of 4
            if random.random() < 0.9:  # 90% chance instead of 80%
                if random.random() < 0.7:  # 70% chance for winning team
                    team_stats = self.winner_stats
                else:
                    team_stats = self.loser_stats
                
                event_time = minute + random.randint(-2, 2)
                player = random.choice(list(team_stats.player_stats.keys()))
                
                event_type = random.choice([
                    EventType.BARON_SECURED,
                    EventType.INHIBITOR_DESTROYED,
                    EventType.TEAM_FIGHT_WIN,
                    EventType.OBJECTIVE_STEAL,
                    EventType.TOWER_DESTROYED
                ])
                
                events.append(MatchEvent(
                    type=event_type,
                    time=event_time,
                    description=self._generate_event_description(event_type, player, team_stats.team),
                    player=player,
                    team=team_stats.team
                ))
        
        # Final victory event
        events.append(MatchEvent(
            type=EventType.TEAM_FIGHT_WIN,
            time=self.game_duration,
            description=f"{self.winner_stats.team.name} wins the game after a decisive team fight!",
            team=self.winner_stats.team
        ))
        
        # Sort events by time
        events.sort(key=lambda e: e.time)
        return events
    
    def _generate_event_description(self, event_type: EventType, player: Player, team: Team) -> str:
        """Generate a descriptive message for a match event."""
        if event_type == EventType.SOLO_KILL:
            if player.role == Role.JUNGLE:
                location = random.choice(["in the river", "during a gank", "at the objective"])
            else:
                location = f"in the {player.role.value} lane"
            return f"{player.name} secures a clean solo kill {location}!"
            
        elif event_type == EventType.OBJECTIVE_STEAL:
            objective = random.choice(["Baron", "Dragon", "Rift Herald"])
            return f"Incredible! {player.name} steals {objective} for {team.name}!"
            
        elif event_type == EventType.TOWER_DESTROYED:
            locations = ["outer", "inner", "inhibitor"]
            lanes = ["top", "mid", "bottom"]
            tower = f"{random.choice(locations)} {random.choice(lanes)} tower"
            return f"{team.name} takes down the {tower}"
            
        elif event_type == EventType.DRAGON_SECURED:
            return f"{team.name} secures the dragon with {player.name} leading the charge!"
            
        elif event_type == EventType.BARON_SECURED:
            minutes = random.randint(20, 35)
            return f"{minutes} min Baron secured by {team.name}, {player.name} dealt the final damage"
            
        elif event_type == EventType.TEAM_FIGHT_WIN:
            locations = [
                "around Baron",
                "at Dragon pit",
                "in the river",
                f"in {player.role.value}",
                "in the enemy jungle"
            ]
            return f"{team.name} wins a crucial team fight {random.choice(locations)} with {player.name} leading the charge!"
            
        elif event_type == EventType.INHIBITOR_DESTROYED:
            lanes = ["top", "mid", "bottom"]
            lane = random.choice(lanes)
            return f"{team.name} breaks the {lane} inhibitor, opening up the base"
            
        elif event_type == EventType.OUTPLAY:
            if player.role == Role.JUNGLE:
                location = random.choice(["in the river", "during a gank", "at the objective"])
            else:
                location = f"in the {player.role.value} lane"
            return f"{player.name} pulls off an incredible outplay {location}!"
            
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
            
        return f"{player.name} makes a great play for {team.name}"
    
    def _generate_dragon_event_description(self, dragon_type: DragonType, player: Player, team: Team) -> str:
        """Generate a descriptive message for a dragon event."""
        if dragon_type == DragonType.ELDER:
            return f"{team.name} secures the Elder Dragon with {player.name} leading the charge!"
        
        # Check if this dragon gives soul
        dragon_state = self.winner_stats.dragon_state if team == self.winner_stats.team else self.loser_stats.dragon_state
        total_dragons = (dragon_state.infernal_stacks + dragon_state.ocean_stacks + 
                        dragon_state.mountain_stacks + dragon_state.cloud_stacks)
        
        if total_dragons == 3:  # This will be the soul
            return f"{team.name} claims the {dragon_type.value} Dragon Soul with {player.name} securing the final dragon!"
        else:
            buff_descriptions = {
                DragonType.INFERNAL: "increasing their team's damage",
                DragonType.OCEAN: "boosting their sustain",
                DragonType.MOUNTAIN: "strengthening their defenses",
                DragonType.CLOUD: "enhancing their mobility"
            }
            return f"{team.name} secures the {dragon_type.value} Dragon, {buff_descriptions[dragon_type]}! {player.name} gets the last hit!"
    
    def update_game_time(self):
        """Update the game timer and check for events."""
        # Update time
        self.current_time += 0.25  # Since we update every 250ms
        minutes = int(self.current_time)
        seconds = int((self.current_time % 1) * 60)
        
        # Update UI
        self.time_label.setText(f"{minutes}:{seconds:02d}")
        self.progress_bar.setValue(minutes)
        
        # Update CS every minute
        if minutes > self.last_cs_update:
            self.last_cs_update = minutes
            # Update CS for both teams
            for team_stats in [self.winner_stats, self.loser_stats]:
                for player in team_stats.player_stats:
                    # Base CS per minute rates for different roles (with some randomization)
                    if player.role in [Role.ADC, Role.MID]:
                        cs_gain = random.randint(8, 10)  # 8-10 CS/min for carries
                    elif player.role == Role.TOP:
                        cs_gain = random.randint(7, 9)   # 7-9 CS/min for top
                    elif player.role == Role.JUNGLE:
                        cs_gain = random.randint(6, 8)   # 6-8 CS/min for jungle
                    else:  # SUPPORT
                        cs_gain = random.randint(0, 1)   # 0-1 CS/min for support
                    
                    # Update CS
                    team_stats.player_stats[player].cs += cs_gain
                    # Add gold from CS (average 19 gold per minion)
                    cs_gold = cs_gain * 19
                    team_stats.player_stats[player].gold_earned += cs_gold
                    team_stats.total_gold += cs_gold
        
        # Check for events
        while (self.next_event_index < len(self.events) and 
               self.events[self.next_event_index].time <= minutes):
            event = self.events[self.next_event_index]
            self.add_event(event)
            
            # Update stats based on event type
            if event.team == self.winner_stats.team:
                team_stats = self.winner_stats
                enemy_stats = self.loser_stats
            else:
                team_stats = self.loser_stats
                enemy_stats = self.winner_stats
            
            if event.type == EventType.SOLO_KILL:
                team_stats.kills += 1
                enemy_stats.deaths += 1
                if event.player:
                    # Update killer stats
                    team_stats.player_stats[event.player].kills += 1
                    team_stats.player_stats[event.player].gold_earned += 300
                    
                    # Pick a random enemy to die
                    dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                    enemy_stats.player_stats[dead_player].deaths += 1
                    
            elif event.type == EventType.TOWER_DESTROYED:
                team_stats.towers += 1
                team_stats.total_gold += 500
                if event.player:
                    team_stats.player_stats[event.player].gold_earned += 150
                    
            elif event.type == EventType.DRAGON_SECURED:
                team_stats.dragons += 1
                team_stats.total_gold += 300
                # Potential team fight at dragon
                if random.random() < 0.4:  # 40% chance of fight
                    self._simulate_small_team_fight(team_stats, enemy_stats)
                    
            elif event.type == EventType.BARON_SECURED:
                team_stats.barons += 1
                team_stats.total_gold += 600
                # Almost always a team fight at baron
                if random.random() < 0.8:  # 80% chance of fight
                    self._simulate_team_fight(team_stats, enemy_stats)
                    
            elif event.type == EventType.TEAM_FIGHT_WIN:
                self._simulate_team_fight(team_stats, enemy_stats)
                
            elif event.type == EventType.OBJECTIVE_STEAL:
                # Stealing team gets the objective and usually triggers a team fight
                team_stats.total_gold += 450  # Average between dragon/herald (300) and baron (600)
                if random.random() < 0.6:  # 60% chance of fight after steal
                    self._simulate_team_fight(team_stats, enemy_stats)
                
            elif event.type == EventType.JUNGLE_INVADE:
                # Successful invade usually results in a small skirmish
                if event.player and event.player.role == Role.JUNGLE:
                    team_stats.total_gold += 200  # Stolen camps value
                if random.random() < 0.4:  # 40% chance of fight
                    self._simulate_small_team_fight(team_stats, enemy_stats)
                
            elif event.type == EventType.COUNTER_GANK:
                # Counter gank usually results in a kill or two
                if event.player:
                    team_stats.kills += 1
                    enemy_stats.deaths += 1
                    team_stats.player_stats[event.player].kills += 1
                    team_stats.player_stats[event.player].gold_earned += 300
                    
                    # Pick a random enemy to die
                    dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                    enemy_stats.player_stats[dead_player].deaths += 1
                    
                    # Add assist for the laner
                    if event.player.role == Role.JUNGLE:
                        # Find the laner in that lane
                        laners = [p for p in team_stats.player_stats.keys() if p.role != Role.JUNGLE]
                        if laners:
                            assister = random.choice(laners)
                            team_stats.player_stats[assister].assists += 1
                            team_stats.player_stats[assister].gold_earned += 150
                
            elif event.type == EventType.OUTPLAY:
                # Outplay usually results in a kill and some gold
                if event.player:
                    team_stats.kills += 1
                    enemy_stats.deaths += 1
                    team_stats.player_stats[event.player].assists += 1  # Outplay bonus
                    team_stats.player_stats[event.player].gold_earned += 450
                    
                    # Pick a random enemy to die
                    dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                    enemy_stats.player_stats[dead_player].deaths += 1
            
            elif event.type == EventType.TOP_SPLIT_PUSH:
                # Split push leads to tower/inhibitor damage and gold
                team_stats.total_gold += 350  # Tower plates + minions
                if random.random() < 0.4:  # 40% chance to get tower
                    team_stats.towers += 1
                    team_stats.total_gold += 500
                if event.player:
                    team_stats.player_stats[event.player].gold_earned += 200
                    
            elif event.type == EventType.MID_ROAM:
                # Successful roam usually results in a kill or objective
                if event.player:
                    team_stats.kills += 1
                    enemy_stats.deaths += 1
                    team_stats.player_stats[event.player].assists += 1  # Roamer usually gets assist
                    team_stats.player_stats[event.player].gold_earned += 150
                    
                    # Find a side lane player to get the kill
                    side_laners = [p for p in team_stats.player_stats.keys() 
                                 if p.role in [Role.TOP, Role.ADC]]
                    if side_laners:
                        killer = random.choice(side_laners)
                        team_stats.player_stats[killer].kills += 1
                        team_stats.player_stats[killer].gold_earned += 300
                    
                    # Pick a random enemy to die
                    dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                    enemy_stats.player_stats[dead_player].deaths += 1
                    
            elif event.type == EventType.ADC_KITING:
                # Perfect kiting usually results in kills without dying
                if event.player:
                    kills = random.randint(1, 2)
                    team_stats.kills += kills
                    enemy_stats.deaths += kills
                    team_stats.player_stats[event.player].kills += kills
                    team_stats.player_stats[event.player].gold_earned += kills * 300
                    
                    # Pick random enemies to die
                    dead_players = random.sample(list(enemy_stats.player_stats.keys()), kills)
                    for dead_player in dead_players:
                        enemy_stats.player_stats[dead_player].deaths += 1
                    
            elif event.type == EventType.SUPPORT_VISION:
                # Vision control leads to picks and objective control
                team_stats.total_gold += 150  # Vision score gold
                if event.player:
                    team_stats.player_stats[event.player].vision_score += random.randint(5, 10)
                    if random.random() < 0.3:  # 30% chance to get a pick
                        # Random carry gets a kill
                        carries = [p for p in team_stats.player_stats.keys() if p.role in [Role.MID, Role.ADC]]
                        if carries:
                            killer = random.choice(carries)
                            team_stats.kills += 1
                            team_stats.player_stats[killer].kills += 1
                            team_stats.player_stats[event.player].assists += 1
                            team_stats.total_gold += 300
                            team_stats.player_stats[killer].gold_earned += 300
                            
                            # Pick a random enemy to die
                            dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                            enemy_stats.player_stats[dead_player].deaths += 1
                    
            elif event.type == EventType.SUPPORT_SAVE:
                # Clutch save prevents a death and might turn a fight
                if event.player:
                    team_stats.player_stats[event.player].assists += 1
                    team_stats.total_gold += 150
                    team_stats.player_stats[event.player].gold_earned += 150
                    
                    if random.random() < 0.5:  # 50% chance to turn the fight
                        # Carry gets a kill
                        carries = [p for p in team_stats.player_stats.keys() if p.role in [Role.MID, Role.ADC]]
                        if carries:
                            killer = random.choice(carries)
                            team_stats.kills += 1
                            team_stats.player_stats[killer].kills += 1
                            team_stats.total_gold += 300
                            team_stats.player_stats[killer].gold_earned += 300
                            
                            # Pick a random enemy to die
                            dead_player = random.choice(list(enemy_stats.player_stats.keys()))
                            enemy_stats.player_stats[dead_player].deaths += 1
                    
            elif event.type == EventType.JUNGLE_OBJECTIVE:
                # Multiple objectives secured
                objectives = random.randint(2, 3)
                team_stats.total_gold += objectives * 200
                if event.player:
                    team_stats.player_stats[event.player].gold_earned += objectives * 100
                    # Random objective types
                    for _ in range(objectives):
                        if random.random() < 0.3:  # 30% for major objective
                            team_stats.barons += 1
                        else:  # 70% for dragon
                            team_stats.dragons += 1
            
            # Update UI
            self.update_stats(self.winner_stats, self.loser_stats)
            
            self.next_event_index += 1
        
        # Check if game is over
        if minutes >= self.game_duration:
            self.game_timer.stop()
            # Select MVP based on final stats
            self.match.result.mvp = max(
                list(self.winner_stats.player_stats.keys()),
                key=lambda p: (
                    self.winner_stats.player_stats[p].kills * 3 +
                    self.winner_stats.player_stats[p].assists * 1.5 +
                    self.winner_stats.player_stats[p].cs * 0.1
                )
            )
            self.match_completed.emit(self.match)

    def _simulate_team_fight(self, winning_team: TeamMatchStats, losing_team: TeamMatchStats):
        """Simulate a full team fight with kills, deaths, and assists."""
        # 3-5 kills in a big team fight
        kills = random.randint(3, 5)
        winning_team.kills += kills
        losing_team.deaths += kills
        
        # Distribute kills among winning team (carry roles more likely to get kills)
        carry_players = [p for p in winning_team.player_stats.keys() if p.role in [Role.ADC, Role.MID]]
        other_players = [p for p in winning_team.player_stats.keys() if p.role not in [Role.ADC, Role.MID]]
        
        for _ in range(kills):
            # 70% chance for carry to get the kill
            if carry_players and random.random() < 0.7:
                killer = random.choice(carry_players)
            else:
                killer = random.choice(other_players if other_players else carry_players)
            
            # Kill gold: 300 base + 30 per kill in streak (capped at 600)
            kill_gold = min(300 + (winning_team.player_stats[killer].kills * 30), 600)
            winning_team.player_stats[killer].kills += 1
            winning_team.player_stats[killer].gold_earned += kill_gold
            winning_team.total_gold += kill_gold
            
            # 2-3 assists per kill
            assisters = random.sample(
                [p for p in winning_team.player_stats.keys() if p != killer],
                min(random.randint(2, 3), len(winning_team.player_stats) - 1)
            )
            for assister in assisters:
                winning_team.player_stats[assister].assists += 1
                assist_gold = 150  # Base assist gold
                winning_team.player_stats[assister].gold_earned += assist_gold
                winning_team.total_gold += assist_gold
        
        # Distribute deaths among losing team (supports and carries slightly less likely to die)
        available_players = list(losing_team.player_stats.keys())
        for _ in range(kills):
            weights = [0.7 if p.role in [Role.SUPPORT, Role.ADC] else 1.0 for p in available_players]
            dead_player = random.choices(available_players, weights=weights, k=1)[0]
            losing_team.player_stats[dead_player].deaths += 1
            
    def _simulate_small_team_fight(self, winning_team: TeamMatchStats, losing_team: TeamMatchStats):
        """Simulate a smaller skirmish (e.g., at dragon) with fewer kills."""
        # 1-2 kills in a small fight
        kills = random.randint(1, 2)
        winning_team.kills += kills
        losing_team.deaths += kills
        
        # Similar to full team fight but with fewer kills
        carry_players = [p for p in winning_team.player_stats.keys() if p.role in [Role.ADC, Role.MID]]
        other_players = [p for p in winning_team.player_stats.keys() if p.role not in [Role.ADC, Role.MID]]
        
        for _ in range(kills):
            if carry_players and random.random() < 0.6:  # Slightly lower chance than full team fight
                killer = random.choice(carry_players)
            else:
                killer = random.choice(other_players if other_players else carry_players)
            
            # Kill gold: 300 base + 30 per kill in streak (capped at 600)
            kill_gold = min(300 + (winning_team.player_stats[killer].kills * 30), 600)
            winning_team.player_stats[killer].kills += 1
            winning_team.player_stats[killer].gold_earned += kill_gold
            winning_team.total_gold += kill_gold
            
            # 1-2 assists per kill in smaller fights
            assisters = random.sample(
                [p for p in winning_team.player_stats.keys() if p != killer],
                min(random.randint(1, 2), len(winning_team.player_stats) - 1)
            )
            for assister in assisters:
                winning_team.player_stats[assister].assists += 1
                assist_gold = 150  # Base assist gold
                winning_team.player_stats[assister].gold_earned += assist_gold
                winning_team.total_gold += assist_gold
        
        # Distribute deaths
        available_players = list(losing_team.player_stats.keys())
        for _ in range(kills):
            dead_player = random.choice(available_players)
            losing_team.player_stats[dead_player].deaths += 1
