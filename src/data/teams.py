from datetime import date
from src.models.team import Team
from src.models.player import Player, Role, PlayerStats
from src.data.lec_teams import create_lec_teams
from src.data.lck_teams import create_lck_teams
from src.data.lpl_teams import create_lpl_teams

def create_na_teams() -> dict[str, Team]:
    """Create and return a dictionary of NA teams with their rosters."""
    teams = {}
    
    # 100 Thieves
    team_100t = Team(
        name="100 Thieves (NA)",
        region="NA",
        budget=11000000,
        fanbase=750000,
        championships=1,
        training_facilities=80,
        brand_value=9500000
    )
    
    team_100t.add_player(Player(
        name="Ssumday",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=80, leadership=85),
        nationality="Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    team_100t.add_player(Player(
        name="Closer",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=85, communication=82, leadership=80),
        nationality="Turkey",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    team_100t.add_player(Player(
        name="Abbedagge",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=86, communication=80, leadership=75),
        nationality="Germany",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    team_100t.add_player(Player(
        name="FBI",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=84, communication=82, leadership=78),
        nationality="Australia",
        salary=430000,
        contract_end=date(2024, 11, 21)
    ))
    
    team_100t.add_player(Player(
        name="Busio",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=80, communication=78, leadership=75),
        nationality="USA",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["100 Thieves (NA)"] = team_100t

    # Cloud9
    c9 = Team(
        name="Cloud9 (NA)",
        region="NA",
        budget=12000000,
        fanbase=900000,
        championships=5,
        training_facilities=90,
        brand_value=11000000
    )
    
    c9.add_player(Player(
        name="Fudge",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=85, communication=82, leadership=80),
        nationality="Australia",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Blaber",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=88, communication=85, leadership=88),
        nationality="USA",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Diplex",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=78, leadership=75),
        nationality="Germany",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Berserker",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=88, communication=75, leadership=78),
        nationality="Korea",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Zven",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=88, communication=85, leadership=88),
        nationality="Denmark",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Cloud9 (NA)"] = c9

    # Team Liquid
    tl = Team(
        name="Team Liquid (NA)",
        region="NA",
        budget=12500000,
        fanbase=850000,
        championships=4,
        training_facilities=95,
        brand_value=12000000
    )
    
    tl.add_player(Player(
        name="Summit",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=86, communication=78, leadership=80),
        nationality="Korea",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="Pyosik",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=80, leadership=78),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="APA",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=82, communication=80, leadership=75),
        nationality="USA",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="Yeon",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=82, leadership=78),
        nationality="USA",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="CoreJJ",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=90, communication=88, leadership=90),
        nationality="Korea",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Team Liquid (NA)"] = tl

    # Evil Geniuses
    eg = Team(
        name="Evil Geniuses (NA)",
        region="NA",
        budget=10500000,
        fanbase=600000,
        championships=1,
        training_facilities=85,
        brand_value=9000000
    )
    
    eg.add_player(Player(
        name="Impact",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=90, communication=85, leadership=88),
        nationality="Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Inspired",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=88, communication=82, leadership=80),
        nationality="Poland",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Jojopyun",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=84, communication=82, leadership=78),
        nationality="Canada",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Kaori",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=80, leadership=75),
        nationality="Turkey",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Vulcan",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=88, leadership=85),
        nationality="Canada",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Evil Geniuses (NA)"] = eg

    # FlyQuest
    fly = Team(
        name="FlyQuest (NA)",
        region="NA",
        budget=9500000,
        fanbase=450000,
        championships=0,
        training_facilities=75,
        brand_value=8000000
    )
    
    fly.add_player(Player(
        name="Impact",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=88, communication=83, leadership=85),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Spica",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=85, leadership=83),
        nationality="USA",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="VicLa",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=84, communication=80, leadership=78),
        nationality="Korea",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Prince",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=85, communication=78, leadership=77),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Eyla",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=84, communication=82, leadership=80),
        nationality="Australia",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["FlyQuest (NA)"] = fly

    # TSM
    tsm = Team(
        name="TSM (NA)",
        region="NA",
        budget=11500000,
        fanbase=1000000,
        championships=7,
        training_facilities=88,
        brand_value=12000000
    )
    
    tsm.add_player(Player(
        name="Huni",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=87, communication=83, leadership=82),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Bugi",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=80, leadership=78),
        nationality="Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Ruby",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="China",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Tactical",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=83, communication=82, leadership=78),
        nationality="USA",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Chime",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=83, communication=85, leadership=80),
        nationality="Canada",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["TSM (NA)"] = tsm

    # Golden Guardians
    gg = Team(
        name="Golden Guardians (NA)",
        region="NA",
        budget=9000000,
        fanbase=400000,
        championships=0,
        training_facilities=70,
        brand_value=7500000
    )
    
    gg.add_player(Player(
        name="Licorice",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=86, communication=82, leadership=80),
        nationality="USA",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="River",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=80, leadership=78),
        nationality="Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="Gori",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=84, communication=78, leadership=75),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="Stixxay",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=83, leadership=82),
        nationality="USA",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="huhi",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=86, communication=84, leadership=83),
        nationality="Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Golden Guardians (NA)"] = gg

    # NRG
    nrg = Team(
        name="NRG (NA)",
        region="NA",
        budget=9500000,
        fanbase=350000,
        championships=0,
        training_facilities=75,
        brand_value=7000000
    )
    
    nrg.add_player(Player(
        name="Dhokla",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=83, communication=80, leadership=78),
        nationality="USA",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="Contractz",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=84, communication=82, leadership=80),
        nationality="USA",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="Palafox",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=81, leadership=78),
        nationality="USA",
        salary=370000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="IgNar",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=86, communication=83, leadership=82),
        nationality="Korea",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="FBI",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=80),
        nationality="Australia",
        salary=430000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["NRG (NA)"] = nrg

    # Dignitas
    dig = Team(
        name="Dignitas (NA)",
        region="NA",
        budget=9000000,
        fanbase=300000,
        championships=0,
        training_facilities=70,
        brand_value=6500000
    )
    
    dig.add_player(Player(
        name="Armut",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=82, leadership=80),
        nationality="Turkey",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="eXyu",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=83, communication=80, leadership=78),
        nationality="Croatia",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="Jensen",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=84, leadership=83),
        nationality="Denmark",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="Tomo",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="USA",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="Biofrost",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=83, leadership=82),
        nationality="Canada",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Dignitas (NA)"] = dig

    return teams

def create_default_teams() -> dict[str, Team]:
    """Create and return a dictionary of all teams with their rosters."""
    teams = {}
    teams.update(create_na_teams())
    teams.update(create_lec_teams())
    teams.update(create_lck_teams())
    teams.update(create_lpl_teams())
    return teams
