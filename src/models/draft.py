from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from .team import Team
from .player import Player, Role
from .champion import Champion

class DraftPhase(Enum):
    BAN_PHASE_1 = "First Ban Phase"
    PICK_PHASE_1 = "First Pick Phase"
    BAN_PHASE_2 = "Second Ban Phase"
    PICK_PHASE_2 = "Second Pick Phase"

@dataclass
class DraftPlayer:
    """Simplified player class for draft purposes."""
    role: Role

@dataclass
class DraftPick:
    """Represents a pick in the draft."""
    champion: Champion
    team: Team
    player: DraftPlayer
    pick_number: int

@dataclass
class DraftBan:
    """Represents a ban in the draft."""
    champion: Champion
    team: Team
    ban_number: int

@dataclass
class DraftState:
    blue_team: Team
    red_team: Team
    current_phase: DraftPhase = DraftPhase.BAN_PHASE_1
    picks: List[DraftPick] = field(default_factory=list)
    bans: List[DraftBan] = field(default_factory=list)
    available_champions: Dict[str, Champion] = field(default_factory=dict)
    current_turn: int = 0  # Track the current turn number
    
    def __post_init__(self):
        """Initialize the available champions pool."""
        self.available_champions = {
            # Top lane champions
            "Aatrox": Champion("Aatrox", [Role.TOP]),
            "Camille": Champion("Camille", [Role.TOP]),
            "Darius": Champion("Darius", [Role.TOP]),
            "Fiora": Champion("Fiora", [Role.TOP]),
            "Gangplank": Champion("Gangplank", [Role.TOP]),
            "Garen": Champion("Garen", [Role.TOP]),
            "Gnar": Champion("Gnar", [Role.TOP]),
            "Gwen": Champion("Gwen", [Role.TOP]),
            "Illaoi": Champion("Illaoi", [Role.TOP]),
            "Irelia": Champion("Irelia", [Role.TOP]),
            "Jax": Champion("Jax", [Role.TOP]),
            "Jayce": Champion("Jayce", [Role.TOP, Role.MID]),
            "K'Sante": Champion("K'Sante", [Role.TOP]),
            "Kennen": Champion("Kennen", [Role.TOP]),
            "Kled": Champion("Kled", [Role.TOP]),
            "Malphite": Champion("Malphite", [Role.TOP]),
            "Mordekaiser": Champion("Mordekaiser", [Role.TOP]),
            "Nasus": Champion("Nasus", [Role.TOP]),
            "Ornn": Champion("Ornn", [Role.TOP]),
            "Renekton": Champion("Renekton", [Role.TOP]),
            "Riven": Champion("Riven", [Role.TOP]),
            "Sett": Champion("Sett", [Role.TOP]),
            "Shen": Champion("Shen", [Role.TOP]),
            "Teemo": Champion("Teemo", [Role.TOP]),
            "Urgot": Champion("Urgot", [Role.TOP]),
            
            # Jungle champions
            "Amumu": Champion("Amumu", [Role.JUNGLE]),
            "Bel'Veth": Champion("Bel'Veth", [Role.JUNGLE]),
            "Diana": Champion("Diana", [Role.JUNGLE, Role.MID]),
            "Ekko": Champion("Ekko", [Role.JUNGLE, Role.MID]),
            "Elise": Champion("Elise", [Role.JUNGLE]),
            "Evelynn": Champion("Evelynn", [Role.JUNGLE]),
            "Graves": Champion("Graves", [Role.JUNGLE]),
            "Hecarim": Champion("Hecarim", [Role.JUNGLE]),
            "Jarvan IV": Champion("Jarvan IV", [Role.JUNGLE]),
            "Karthus": Champion("Karthus", [Role.JUNGLE, Role.MID]),
            "Kayn": Champion("Kayn", [Role.JUNGLE]),
            "Kindred": Champion("Kindred", [Role.JUNGLE]),
            "Lee Sin": Champion("Lee Sin", [Role.JUNGLE]),
            "Master Yi": Champion("Master Yi", [Role.JUNGLE]),
            "Nidalee": Champion("Nidalee", [Role.JUNGLE]),
            "Nocturne": Champion("Nocturne", [Role.JUNGLE]),
            "Nunu & Willump": Champion("Nunu & Willump", [Role.JUNGLE]),
            "Rammus": Champion("Rammus", [Role.JUNGLE]),
            "Rek'Sai": Champion("Rek'Sai", [Role.JUNGLE]),
            "Sejuani": Champion("Sejuani", [Role.JUNGLE]),
            "Shaco": Champion("Shaco", [Role.JUNGLE]),
            "Vi": Champion("Vi", [Role.JUNGLE]),
            "Viego": Champion("Viego", [Role.JUNGLE]),
            "Warwick": Champion("Warwick", [Role.JUNGLE]),
            "Xin Zhao": Champion("Xin Zhao", [Role.JUNGLE]),
            
            # Mid lane champions
            "Ahri": Champion("Ahri", [Role.MID]),
            "Akali": Champion("Akali", [Role.MID, Role.TOP]),
            "Anivia": Champion("Anivia", [Role.MID]),
            "Annie": Champion("Annie", [Role.MID]),
            "Aurelion Sol": Champion("Aurelion Sol", [Role.MID]),
            "Azir": Champion("Azir", [Role.MID]),
            "Cassiopeia": Champion("Cassiopeia", [Role.MID]),
            "Fizz": Champion("Fizz", [Role.MID]),
            "Galio": Champion("Galio", [Role.MID, Role.SUPPORT]),
            "Kassadin": Champion("Kassadin", [Role.MID]),
            "Katarina": Champion("Katarina", [Role.MID]),
            "LeBlanc": Champion("LeBlanc", [Role.MID]),
            "Lissandra": Champion("Lissandra", [Role.MID]),
            "Lux": Champion("Lux", [Role.MID, Role.SUPPORT]),
            "Malzahar": Champion("Malzahar", [Role.MID]),
            "Orianna": Champion("Orianna", [Role.MID]),
            "Ryze": Champion("Ryze", [Role.MID]),
            "Sylas": Champion("Sylas", [Role.MID]),
            "Syndra": Champion("Syndra", [Role.MID]),
            "Twisted Fate": Champion("Twisted Fate", [Role.MID]),
            "Veigar": Champion("Veigar", [Role.MID]),
            "Viktor": Champion("Viktor", [Role.MID]),
            "Xerath": Champion("Xerath", [Role.MID]),
            "Yasuo": Champion("Yasuo", [Role.MID]),
            "Zed": Champion("Zed", [Role.MID]),
            
            # ADC champions
            "Aphelios": Champion("Aphelios", [Role.ADC]),
            "Ashe": Champion("Ashe", [Role.ADC]),
            "Caitlyn": Champion("Caitlyn", [Role.ADC]),
            "Draven": Champion("Draven", [Role.ADC]),
            "Ezreal": Champion("Ezreal", [Role.ADC]),
            "Jhin": Champion("Jhin", [Role.ADC]),
            "Jinx": Champion("Jinx", [Role.ADC]),
            "Kai'Sa": Champion("Kai'Sa", [Role.ADC]),
            "Kalista": Champion("Kalista", [Role.ADC]),
            "Kog'Maw": Champion("Kog'Maw", [Role.ADC]),
            "Lucian": Champion("Lucian", [Role.ADC]),
            "Miss Fortune": Champion("Miss Fortune", [Role.ADC]),
            "Nilah": Champion("Nilah", [Role.ADC]),
            "Samira": Champion("Samira", [Role.ADC]),
            "Senna": Champion("Senna", [Role.ADC, Role.SUPPORT]),
            "Sivir": Champion("Sivir", [Role.ADC]),
            "Tristana": Champion("Tristana", [Role.ADC]),
            "Twitch": Champion("Twitch", [Role.ADC]),
            "Varus": Champion("Varus", [Role.ADC]),
            "Vayne": Champion("Vayne", [Role.ADC]),
            "Xayah": Champion("Xayah", [Role.ADC]),
            "Zeri": Champion("Zeri", [Role.ADC]),
            
            # Support champions
            "Alistar": Champion("Alistar", [Role.SUPPORT]),
            "Bard": Champion("Bard", [Role.SUPPORT]),
            "Blitzcrank": Champion("Blitzcrank", [Role.SUPPORT]),
            "Brand": Champion("Brand", [Role.SUPPORT, Role.MID]),
            "Braum": Champion("Braum", [Role.SUPPORT]),
            "Janna": Champion("Janna", [Role.SUPPORT]),
            "Karma": Champion("Karma", [Role.SUPPORT]),
            "Leona": Champion("Leona", [Role.SUPPORT]),
            "Lulu": Champion("Lulu", [Role.SUPPORT]),
            "Morgana": Champion("Morgana", [Role.SUPPORT, Role.MID]),
            "Nami": Champion("Nami", [Role.SUPPORT]),
            "Nautilus": Champion("Nautilus", [Role.SUPPORT]),
            "Pyke": Champion("Pyke", [Role.SUPPORT]),
            "Rakan": Champion("Rakan", [Role.SUPPORT]),
            "Renata Glasc": Champion("Renata Glasc", [Role.SUPPORT]),
            "Sona": Champion("Sona", [Role.SUPPORT]),
            "Soraka": Champion("Soraka", [Role.SUPPORT]),
            "Tahm Kench": Champion("Tahm Kench", [Role.SUPPORT, Role.TOP]),
            "Taric": Champion("Taric", [Role.SUPPORT]),
            "Thresh": Champion("Thresh", [Role.SUPPORT]),
            "Yuumi": Champion("Yuumi", [Role.SUPPORT]),
            "Zilean": Champion("Zilean", [Role.SUPPORT, Role.MID]),
            "Zyra": Champion("Zyra", [Role.SUPPORT])
        }
    
    def get_available_champions(self, filter_text: str = "", role: Role = None) -> List[Champion]:
        """Get a list of available champions, optionally filtered by text and role."""
        champions = list(self.available_champions.values())
        
        if filter_text:
            filter_text = filter_text.lower()
            champions = [c for c in champions if filter_text in c.name.lower()]
            
        if role:
            champions = [c for c in champions if role in c.roles]
            
        return champions

    def get_current_team(self) -> Team:
        """Get the team whose turn it is."""
        # Ban Phase 1: Blue, Red, Blue, Red, Blue, Red
        if self.current_phase == DraftPhase.BAN_PHASE_1:
            blue_bans = len([b for b in self.bans if b.team == self.blue_team and b.ban_number <= 3])
            red_bans = len([b for b in self.bans if b.team == self.red_team and b.ban_number <= 3])
            return self.blue_team if blue_bans == red_bans else self.red_team
            
        # Pick Phase 1: Blue, Red, Red, Blue, Blue, Red
        elif self.current_phase == DraftPhase.PICK_PHASE_1:
            picks = len(self.picks)
            if picks == 0: return self.blue_team  # First pick
            if picks == 1: return self.red_team   # Second pick
            if picks == 2: return self.red_team   # Third pick
            if picks == 3: return self.blue_team  # Fourth pick
            if picks == 4: return self.blue_team  # Fifth pick
            return self.red_team                  # Sixth pick
            
        # Ban Phase 2: Red, Red, Blue, Blue
        elif self.current_phase == DraftPhase.BAN_PHASE_2:
            phase2_bans = [b for b in self.bans if b.ban_number > 3]
            num_bans = len(phase2_bans)
            if num_bans < 2:  # First two bans are Red
                return self.red_team
            else:  # Last two bans are Blue
                return self.blue_team
                
        # Pick Phase 2: Red, Blue, Red, Blue
        elif self.current_phase == DraftPhase.PICK_PHASE_2:
            phase2_picks = len(self.picks) - 6  # Subtract phase 1 picks
            if phase2_picks == 0: return self.red_team   # First pick
            if phase2_picks == 1: return self.blue_team  # Second pick
            if phase2_picks == 2: return self.red_team   # Third pick
            return self.blue_team                        # Fourth pick
            
        return None

    def get_next_role_to_pick(self, team: Team) -> Optional[Role]:
        """Get the next role that needs to be picked for the team."""
        picked_roles = {pick.player.role for pick in self.picks if pick.team == team}
        all_roles = set(Role)
        available_roles = all_roles - picked_roles
        return next(iter(available_roles)) if available_roles else None
    
    def is_valid_pick(self, champion: Champion, team: Team) -> bool:
        """Check if a champion can be picked by the team."""
        if not isinstance(champion, Champion):
            return False
            
        if champion.banned or champion.picked:
            return False
            
        # Check if it's the team's turn
        if team != self.get_current_team():
            return False
            
        # Check if we're in a pick phase
        if self.current_phase not in [DraftPhase.PICK_PHASE_1, DraftPhase.PICK_PHASE_2]:
            return False
            
        # Check if the champion can play the needed role
        next_role = self.get_next_role_to_pick(team)
        if not next_role or next_role not in champion.roles:
            return False
            
        return True
    
    def is_valid_ban(self, champion: Champion, team: Team) -> bool:
        """Check if a champion can be banned by the team."""
        if not isinstance(champion, Champion):
            return False
            
        if champion.banned or champion.picked:
            return False
            
        # Check if it's the team's turn
        if team != self.get_current_team():
            return False
            
        # Check if we're in a ban phase
        if self.current_phase not in [DraftPhase.BAN_PHASE_1, DraftPhase.BAN_PHASE_2]:
            return False
            
        return True
    
    def make_pick(self, champion: Champion, team: Team) -> bool:
        """Make a pick for the given team."""
        if not self.is_valid_pick(champion, team):
            return False
            
        # Calculate pick number (1-5 for each team)
        team_picks = [p for p in self.picks if p.team == team]
        pick_number = len(team_picks) + 1
            
        # Get the next role to pick
        role = self.get_next_role_to_pick(team)
        if not role:
            return False
            
        # Create draft player and pick
        player = DraftPlayer(role=role)
        pick = DraftPick(champion=champion, team=team, player=player, pick_number=pick_number)
        
        self.picks.append(pick)
        champion.picked = True
        
        # Update phase if needed
        if self.current_phase == DraftPhase.PICK_PHASE_1:
            if len(self.picks) == 6:  # After 6 picks, move to ban phase 2
                self.current_phase = DraftPhase.BAN_PHASE_2
        elif self.current_phase == DraftPhase.PICK_PHASE_2:
            if len(self.picks) == 10:  # After all 10 picks, draft is complete
                self.current_phase = None
                
        return True

    def make_ban(self, champion: Champion, team: Team) -> bool:
        """Make a ban for the given team."""
        if not self.is_valid_ban(champion, team):
            return False
            
        # Calculate ban number (1-3 for first phase, 4-5 for second phase)
        if self.current_phase == DraftPhase.BAN_PHASE_1:
            team_bans = [b for b in self.bans if b.team == team and b.ban_number <= 3]
            ban_number = len(team_bans) + 1
        else:  # BAN_PHASE_2
            team_bans = [b for b in self.bans if b.team == team and b.ban_number > 3]
            ban_number = len(team_bans) + 4
            
        # Create and add the ban
        ban = DraftBan(champion=champion, team=team, ban_number=ban_number)
        self.bans.append(ban)
        champion.banned = True
        
        # Update phase if needed
        if self.current_phase == DraftPhase.BAN_PHASE_1:
            if len([b for b in self.bans if b.ban_number <= 3]) == 6:
                self.current_phase = DraftPhase.PICK_PHASE_1
        elif self.current_phase == DraftPhase.BAN_PHASE_2:
            if len([b for b in self.bans if b.ban_number > 3]) == 4:
                self.current_phase = DraftPhase.PICK_PHASE_2
                
        return True

    def _update_phase(self):
        """Update the draft phase based on current turn."""
        if self.current_phase == DraftPhase.BAN_PHASE_1 and len([b for b in self.bans if b.ban_number <= 3]) == 6:
            self.current_phase = DraftPhase.PICK_PHASE_1
            self.current_turn = 0
            
        elif self.current_phase == DraftPhase.PICK_PHASE_1 and len(self.picks) == 6:
            self.current_phase = DraftPhase.BAN_PHASE_2
            self.current_turn = 0
            
        elif self.current_phase == DraftPhase.BAN_PHASE_2 and len([b for b in self.bans if b.ban_number > 3]) == 4:
            self.current_phase = DraftPhase.PICK_PHASE_2
            self.current_turn = 0
            
        elif self.current_phase == DraftPhase.PICK_PHASE_2 and len(self.picks) == 10:
            self.current_phase = None  # Draft complete
