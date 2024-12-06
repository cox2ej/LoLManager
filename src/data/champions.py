from typing import Dict
from src.models.champion import Champion
from src.models.player import Role

def get_all_champions() -> Dict[str, Champion]:
    """Get all available champions with their roles."""
    champions = {}
    
    # Top lane champions
    top_champions = [
        ("Aatrox", {Role.TOP}),
        ("Camille", {Role.TOP}),
        ("Darius", {Role.TOP}),
        ("Fiora", {Role.TOP}),
        ("Garen", {Role.TOP}),
        ("Gnar", {Role.TOP}),
        ("Irelia", {Role.TOP, Role.MID}),
        ("Jax", {Role.TOP, Role.JUNGLE}),
        ("Jayce", {Role.TOP, Role.MID}),
        ("Kennen", {Role.TOP, Role.MID}),
        ("Malphite", {Role.TOP}),
        ("Mordekaiser", {Role.TOP}),
        ("Nasus", {Role.TOP}),
        ("Ornn", {Role.TOP}),
        ("Renekton", {Role.TOP}),
        ("Riven", {Role.TOP}),
        ("Sett", {Role.TOP}),
        ("Shen", {Role.TOP}),
        ("Teemo", {Role.TOP}),
        ("Urgot", {Role.TOP}),
    ]
    
    # Jungle champions
    jungle_champions = [
        ("Amumu", {Role.JUNGLE}),
        ("Elise", {Role.JUNGLE}),
        ("Evelynn", {Role.JUNGLE}),
        ("Graves", {Role.JUNGLE}),
        ("Hecarim", {Role.JUNGLE}),
        ("Jarvan IV", {Role.JUNGLE}),
        ("Kayn", {Role.JUNGLE}),
        ("Kha'Zix", {Role.JUNGLE}),
        ("Lee Sin", {Role.JUNGLE}),
        ("Master Yi", {Role.JUNGLE}),
        ("Nidalee", {Role.JUNGLE}),
        ("Nocturne", {Role.JUNGLE}),
        ("Nunu & Willump", {Role.JUNGLE}),
        ("Rammus", {Role.JUNGLE}),
        ("Rek'Sai", {Role.JUNGLE}),
        ("Sejuani", {Role.JUNGLE}),
        ("Vi", {Role.JUNGLE}),
        ("Warwick", {Role.JUNGLE}),
        ("Xin Zhao", {Role.JUNGLE}),
        ("Zac", {Role.JUNGLE}),
    ]
    
    # Mid lane champions
    mid_champions = [
        ("Ahri", {Role.MID}),
        ("Akali", {Role.MID, Role.TOP}),
        ("Anivia", {Role.MID}),
        ("Annie", {Role.MID}),
        ("Azir", {Role.MID}),
        ("Cassiopeia", {Role.MID}),
        ("Diana", {Role.MID, Role.JUNGLE}),
        ("Fizz", {Role.MID}),
        ("Katarina", {Role.MID}),
        ("LeBlanc", {Role.MID}),
        ("Lux", {Role.MID, Role.SUPPORT}),
        ("Malzahar", {Role.MID}),
        ("Orianna", {Role.MID}),
        ("Sylas", {Role.MID}),
        ("Syndra", {Role.MID}),
        ("Twisted Fate", {Role.MID}),
        ("Veigar", {Role.MID}),
        ("Viktor", {Role.MID}),
        ("Yasuo", {Role.MID}),
        ("Zed", {Role.MID}),
    ]
    
    # ADC champions
    adc_champions = [
        ("Ashe", {Role.ADC}),
        ("Caitlyn", {Role.ADC}),
        ("Draven", {Role.ADC}),
        ("Ezreal", {Role.ADC}),
        ("Jhin", {Role.ADC}),
        ("Jinx", {Role.ADC}),
        ("Kai'Sa", {Role.ADC}),
        ("Kalista", {Role.ADC}),
        ("Kog'Maw", {Role.ADC}),
        ("Lucian", {Role.ADC}),
        ("Miss Fortune", {Role.ADC}),
        ("Samira", {Role.ADC}),
        ("Senna", {Role.ADC, Role.SUPPORT}),
        ("Sivir", {Role.ADC}),
        ("Tristana", {Role.ADC}),
        ("Twitch", {Role.ADC}),
        ("Vayne", {Role.ADC}),
        ("Varus", {Role.ADC}),
        ("Xayah", {Role.ADC}),
        ("Zeri", {Role.ADC}),
    ]
    
    # Support champions
    support_champions = [
        ("Alistar", {Role.SUPPORT}),
        ("Bard", {Role.SUPPORT}),
        ("Blitzcrank", {Role.SUPPORT}),
        ("Brand", {Role.SUPPORT, Role.MID}),
        ("Braum", {Role.SUPPORT}),
        ("Janna", {Role.SUPPORT}),
        ("Karma", {Role.SUPPORT}),
        ("Leona", {Role.SUPPORT}),
        ("Lulu", {Role.SUPPORT}),
        ("Morgana", {Role.SUPPORT, Role.MID}),
        ("Nami", {Role.SUPPORT}),
        ("Nautilus", {Role.SUPPORT}),
        ("Pyke", {Role.SUPPORT}),
        ("Rakan", {Role.SUPPORT}),
        ("Soraka", {Role.SUPPORT}),
        ("Thresh", {Role.SUPPORT}),
        ("Vel'Koz", {Role.SUPPORT, Role.MID}),
        ("Xerath", {Role.SUPPORT, Role.MID}),
        ("Yuumi", {Role.SUPPORT}),
        ("Zyra", {Role.SUPPORT}),
    ]
    
    # Create Champion objects for all champions
    for name, roles in (top_champions + jungle_champions + mid_champions + 
                       adc_champions + support_champions):
        champions[name] = Champion(name=name, roles=roles)
    
    return champions
