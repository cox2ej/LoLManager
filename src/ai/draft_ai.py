from typing import List, Optional, Dict
from ..models.draft import Champion, DraftState, DraftPhase
from ..models.team import Team
from ..models.player import Role, Player
import random

class DraftAI:
    """AI for making draft choices."""
    
    # Champion tier lists by role (S tier = strongest)
    TIER_LIST = {
        Role.TOP: {
            'S': ['K\'Sante', 'Aatrox', 'Fiora', 'Jax'],
            'A': ['Darius', 'Gwen', 'Camille', 'Sett', 'Gnar'],
            'B': ['Mordekaiser', 'Shen', 'Ornn', 'Gangplank'],
            'C': ['Malphite', 'Teemo', 'Urgot', 'Nasus']
        },
        Role.JUNGLE: {
            'S': ['Bel\'Veth', 'Lee Sin', 'Graves', 'Vi'],
            'A': ['Kayn', 'Viego', 'Kindred', 'Hecarim'],
            'B': ['Sejuani', 'Rammus', 'Warwick', 'Nocturne'],
            'C': ['Amumu', 'Master Yi', 'Shaco', 'Nunu & Willump']
        },
        Role.MID: {
            'S': ['Ahri', 'Akali', 'Viktor', 'Syndra'],
            'A': ['Zed', 'Yasuo', 'Katarina', 'Vex'],
            'B': ['Annie', 'Lux', 'Veigar', 'Malzahar'],
            'C': ['Ryze', 'Twisted Fate', 'Azir', 'Galio']
        },
        Role.ADC: {
            'S': ['Kai\'Sa', 'Jinx', 'Caitlyn', 'Jhin'],
            'A': ['Ezreal', 'Lucian', 'Vayne', 'Tristana'],
            'B': ['Ashe', 'Miss Fortune', 'Xayah', 'Draven'],
            'C': ['Sivir', 'Twitch', 'Kog\'Maw', 'Aphelios']
        },
        Role.SUPPORT: {
            'S': ['Thresh', 'Lulu', 'Nami', 'Pyke'],
            'A': ['Leona', 'Nautilus', 'Soraka', 'Karma'],
            'B': ['Senna', 'Morgana', 'Blitzcrank', 'Janna'],
            'C': ['Yuumi', 'Zilean', 'Taric', 'Braum']
        }
    }
    
    # Champions that work well together
    SYNERGIES = {
        'Yasuo': ['Malphite', 'Diana', 'Gragas'],  # Knockup combos
        'Kalista': ['Thresh', 'Nautilus', 'Leona'],  # Strong engage supports
        'Twitch': ['Lulu', 'Yuumi'],  # Hypercarry enablers
        'Master Yi': ['Taric', 'Kayle'],  # Invulnerability
    }
    
    # Strong counter picks
    COUNTERS = {
        'Katarina': ['Galio', 'Diana', 'Lissandra'],  # CC and tankiness
        'Vayne': ['Caitlyn', 'Draven', 'Miss Fortune'],  # Lane bullies
        'Master Yi': ['Rammus', 'Leona', 'Lissandra'],  # Point-and-click CC
        'Yuumi': ['Leona', 'Nautilus', 'Thresh'],  # Hard engage
    }

    @staticmethod
    def get_pick_choice(draft_state: DraftState, team: Team, role: Role) -> Optional[Champion]:
        """Get the AI's pick choice for the given role."""
        # Get all available champions that can play this role
        available_champions = [
            champ for champ in draft_state.available_champions.values()
            if role in champ.roles and not champ.banned and not champ.picked
        ]
        
        if not available_champions:
            print(f"No available champions for role {role}")
            return None
            
        # Get champions by tier for this role
        tier_champions = {
            'S': [c for c in available_champions if c.name in DraftAI.TIER_LIST[role]['S']],
            'A': [c for c in available_champions if c.name in DraftAI.TIER_LIST[role]['A']],
            'B': [c for c in available_champions if c.name in DraftAI.TIER_LIST[role]['B']],
            'C': [c for c in available_champions if c.name in DraftAI.TIER_LIST[role]['C']]
        }
        
        # Try to pick from each tier, starting with S
        for tier in ['S', 'A', 'B', 'C']:
            if tier_champions[tier]:
                choice = random.choice(tier_champions[tier])
                print(f"AI choosing {choice.name} ({tier} tier) for {role}")
                return choice
                
        # If no tiered champions available, pick randomly from available
        choice = random.choice(available_champions)
        print(f"AI choosing {choice.name} (untiered) for {role}")
        return choice
    
    @staticmethod
    def get_ban_choice(draft_state: DraftState, team: Team) -> Optional[Champion]:
        """Get the AI's ban choice."""
        # Get all available champions that aren't banned or picked
        available_champions = [
            champ for champ in draft_state.available_champions.values()
            if not champ.banned and not champ.picked
        ]
        
        if not available_champions:
            print("No available champions to ban")
            return None
            
        # Collect all S and A tier champions across roles
        high_tier_champions = set()  # Use set to avoid duplicates
        for role in Role:
            high_tier_champions.update(DraftAI.TIER_LIST[role]['S'])
            high_tier_champions.update(DraftAI.TIER_LIST[role]['A'])
            
        # Filter available champions to high tier ones
        ban_candidates = [c for c in available_champions if c.name in high_tier_champions]
        
        if ban_candidates:
            choice = random.choice(ban_candidates)
            print(f"AI banning high-tier champion {choice.name}")
            return choice
            
        # If no high tier champions available, ban randomly
        choice = random.choice(available_champions)
        print(f"AI banning random champion {choice.name}")
        return choice
