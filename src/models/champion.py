from dataclasses import dataclass, field
from typing import List, Set
from src.models.player import Role

@dataclass
class Champion:
    """Represents a champion in the game."""
    name: str
    roles: Set[Role]
    banned: bool = False
    picked: bool = False
