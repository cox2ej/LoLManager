from datetime import date
from src.models.team import Team
from src.models.player import Player, Role, PlayerStats
from src.models.league import League, Division

def create_lec_league() -> League:
    """Create and return the LEC league with all teams."""
    # Create teams
    teams = create_lec_teams()
    
    # Create divisions dictionary
    divisions = {
        "Regular Season": list(teams.values())
    }
    
    # Create and return the league
    return League("LEC", divisions)

def create_lec_teams() -> dict[str, Team]:
    """Create and return a dictionary of LEC teams with their rosters."""
    teams = {}
    
    # G2 Esports
    g2 = Team(
        name="G2 Esports (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=13000000,
        fanbase=1200000,
        championships=9,
        training_facilities=95,
        brand_value=15000000
    )
    
    g2.add_player(Player(
        name="BrokenBlade",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=88, communication=85, leadership=82),
        nationality="Germany",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    g2.add_player(Player(
        name="Yike",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=78),
        nationality="France",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    g2.add_player(Player(
        name="Caps",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=85, leadership=85),
        nationality="Denmark",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    g2.add_player(Player(
        name="Hans Sama",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=83, leadership=80),
        nationality="France",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    g2.add_player(Player(
        name="Mikyx",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=85, leadership=82),
        nationality="Slovenia",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["G2 Esports (EU)"] = g2

    # Fnatic
    fnc = Team(
        name="Fnatic (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=12500000,
        fanbase=1100000,
        championships=7,
        training_facilities=90,
        brand_value=14000000
    )
    
    fnc.add_player(Player(
        name="Oscarinin",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=80, leadership=75),
        nationality="Spain",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    fnc.add_player(Player(
        name="Razork",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="Spain",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    fnc.add_player(Player(
        name="Humanoid",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=83, leadership=80),
        nationality="Czech Republic",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    fnc.add_player(Player(
        name="Noah",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=82, communication=80, leadership=75),
        nationality="Germany",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    fnc.add_player(Player(
        name="Jun",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=78, leadership=75),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Fnatic (EU)"] = fnc

    # MAD Lions
    mad = Team(
        name="MAD Lions (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=10000000,
        fanbase=600000,
        championships=2,
        training_facilities=85,
        brand_value=9000000
    )
    
    mad.add_player(Player(
        name="Chasy",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=78, leadership=75),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    mad.add_player(Player(
        name="Elyoya",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=82),
        nationality="Spain",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    mad.add_player(Player(
        name="Nisqy",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=87, communication=85, leadership=83),
        nationality="Belgium",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    mad.add_player(Player(
        name="Carzzy",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="Czech Republic",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    mad.add_player(Player(
        name="Hylissang",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=88, communication=83, leadership=80),
        nationality="Bulgaria",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["MAD Lions (EU)"] = mad

    # Team Heretics
    heretics = Team(
        name="Team Heretics (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=8000000,
        fanbase=400000,
        championships=0,
        training_facilities=80,
        brand_value=7000000
    )
    
    heretics.add_player(Player(
        name="Evi",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=78),
        nationality="Japan",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    heretics.add_player(Player(
        name="Bo",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=80, leadership=78),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    heretics.add_player(Player(
        name="Ruby",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    heretics.add_player(Player(
        name="Jackspektra",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=82, communication=80, leadership=75),
        nationality="Norway",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    heretics.add_player(Player(
        name="Mersa",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=83, communication=80, leadership=75),
        nationality="Greece",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Team Heretics (EU)"] = heretics

    # Team BDS
    bds = Team(
        name="Team BDS (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=7500000,
        fanbase=300000,
        championships=0,
        training_facilities=75,
        brand_value=6000000
    )
    
    bds.add_player(Player(
        name="Adam",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=82, communication=80, leadership=78),
        nationality="France",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    bds.add_player(Player(
        name="Sheo",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="France",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    bds.add_player(Player(
        name="nuc",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="France",
        salary=280000,
        contract_end=date(2024, 11, 21)
    ))
    
    bds.add_player(Player(
        name="Crownie",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=78),
        nationality="Croatia",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    bds.add_player(Player(
        name="Labrov",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="Greece",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Team BDS (EU)"] = bds

    # SK Gaming
    sk = Team(
        name="SK Gaming (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=8500000,
        fanbase=450000,
        championships=0,
        training_facilities=82,
        brand_value=7500000
    )
    
    sk.add_player(Player(
        name="Irrelevant",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="Germany",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    sk.add_player(Player(
        name="Markoon",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="Netherlands",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    sk.add_player(Player(
        name="Sertuss",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="Germany",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    sk.add_player(Player(
        name="Exakick",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=80, leadership=75),
        nationality="France",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    sk.add_player(Player(
        name="Doss",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=82, communication=80, leadership=75),
        nationality="Denmark",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["SK Gaming (EU)"] = sk

    # Excel
    excel = Team(
        name="Excel (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=8000000,
        fanbase=350000,
        championships=0,
        training_facilities=78,
        brand_value=7000000
    )
    
    excel.add_player(Player(
        name="Odoamne",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=88, communication=85, leadership=85),
        nationality="Romania",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    excel.add_player(Player(
        name="Xerxe",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=82, leadership=80),
        nationality="Romania",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    excel.add_player(Player(
        name="Vetheo",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=84, communication=80, leadership=78),
        nationality="France",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    excel.add_player(Player(
        name="Patrik",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=80),
        nationality="Czech Republic",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    excel.add_player(Player(
        name="Targamas",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=78),
        nationality="France",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Excel (EU)"] = excel

    # Astralis
    astralis = Team(
        name="Astralis (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=7500000,
        fanbase=400000,
        championships=0,
        training_facilities=75,
        brand_value=6500000
    )
    
    astralis.add_player(Player(
        name="Finn",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=80),
        nationality="Sweden",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    astralis.add_player(Player(
        name="113",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="Denmark",
        salary=280000,
        contract_end=date(2024, 11, 21)
    ))
    
    astralis.add_player(Player(
        name="Lider",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=82, communication=78, leadership=75),
        nationality="Norway",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    astralis.add_player(Player(
        name="Kobbe",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=85, communication=83, leadership=82),
        nationality="Denmark",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    astralis.add_player(Player(
        name="JeongHoon",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=78, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Astralis (EU)"] = astralis

    # Team Vitality
    vitality = Team(
        name="Team Vitality (EU)",
        region="EU",  # Keep as EU to match our region mapping
        budget=11000000,
        fanbase=800000,
        championships=1,
        training_facilities=88,
        brand_value=12000000
    )
    
    vitality.add_player(Player(
        name="Photon",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=80, leadership=78),
        nationality="China",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    vitality.add_player(Player(
        name="Bo",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=80, leadership=78),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    vitality.add_player(Player(
        name="Perkz",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=90, communication=88, leadership=90),
        nationality="Croatia",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    vitality.add_player(Player(
        name="Neon",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="Slovakia",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    vitality.add_player(Player(
        name="Kaiser",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=84, leadership=82),
        nationality="Germany",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Team Vitality (EU)"] = vitality

    return teams
