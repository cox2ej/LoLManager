import os
from pathlib import Path
import logging
import sys

class ChampionAssets:
    """Utility class for managing champion assets like portraits."""
    
    @classmethod
    def get_portraits_dir(cls) -> Path:
        """Get the portraits directory path that works in both dev and packaged environments."""
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (packaged with PyInstaller)
            base_path = Path(sys._MEIPASS)
        else:
            # If the application is run from a Python interpreter
            base_path = Path(__file__).parent.parent
            
        return base_path / "ChampionPortraits"
    
    @classmethod
    def get_portrait_path(cls, champion_name: str) -> str:
        """
        Get the path to a champion's portrait.
        
        Args:
            champion_name: The name of the champion (e.g., "Aatrox", "Kai'Sa")
            
        Returns:
            str: Absolute path to the champion's portrait image
            
        Raises:
            FileNotFoundError: If the portrait file doesn't exist
        """
        # Handle special cases
        name_mapping = {
            "Aurelion Sol": "Aurelion_Sol",
            "Bel'Veth": "Bel%27Veth",
            "Cho'Gath": "Cho%27Gath",
            "Dr. Mundo": "Dr._Mundo",
            "Jarvan IV": "Jarvan_IV",
            "Kai'Sa": "Kai%27Sa",
            "Kha'Zix": "Kha%27Zix",
            "Kog'Maw": "Kog%27Maw",
            "K'Sante": "K%27Sante",
            "Lee Sin": "Lee_Sin",
            "Master Yi": "Master_Yi",
            "Miss Fortune": "MissFortune",
            "Nunu & Willump": "Nunu_%26_Willump",
            "Rek'Sai": "Rek%27Sai",
            "Renata Glasc": "Renata_Glasc",
            "Tahm Kench": "Tahm_Kench",
            "Twisted Fate": "Twisted_Fate",
            "Vel'Koz": "Vel%27Koz",
            "Xin Zhao": "Xin_Zhao"
        }
        
        # Map the champion name if it's in our special cases
        formatted_name = name_mapping.get(champion_name, champion_name)
        
        # Handle special characters in the filename
        if champion_name not in name_mapping:
            formatted_name = formatted_name.replace("'", "%27")
            formatted_name = formatted_name.replace(" ", "_")
            formatted_name = formatted_name.replace("&", "%26")
        
        # Create the filename
        filename = f"{formatted_name}Square.webp"
        
        # Get the full path
        portrait_path = cls.get_portraits_dir() / filename
        
        # Check if file exists
        if not portrait_path.exists():
            logging.error(f"Portrait not found for champion {champion_name} at path {portrait_path}")
            raise FileNotFoundError(f"Portrait not found for champion {champion_name}")
            
        return str(portrait_path)
    
    @classmethod
    def is_portrait_available(cls, champion_name: str) -> bool:
        """Check if a portrait is available for the given champion."""
        try:
            cls.get_portrait_path(champion_name)
            return True
        except FileNotFoundError:
            return False
