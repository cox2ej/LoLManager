from datetime import date
from src.models.team import Team
from src.models.player import Player, Role, PlayerStats
from src.models.league import League, Division

def create_lcs_league() -> League:
    """Create and return the LCS league with all teams."""
    # Create teams
    teams = create_lcs_teams()
    
    # Create divisions dictionary
    divisions = {
        "Regular Season": list(teams.values())
    }
    
    # Create and return the league
    return League("LCS", divisions)

def create_lcs_teams() -> dict[str, Team]:
    """Create and return a dictionary of LCS teams with their rosters."""
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
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=80, leadership=75),
        nationality="Australia",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    team_100t.add_player(Player(
        name="Huhi",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=87, communication=85, leadership=80),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["100 Thieves (NA)"] = team_100t
    
    # Cloud9
    c9 = Team(
        name="Cloud9 (NA)",
        region="NA",
        budget=12000000,
        fanbase=900000,
        championships=4,
        training_facilities=85,
        brand_value=11000000
    )
    
    c9.add_player(Player(
        name="Fudge",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=85, leadership=80),
        nationality="Australia",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Blaber",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=87, communication=85, leadership=85),
        nationality="United States",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Jojopyun",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=85, communication=83, leadership=78),
        nationality="Canada",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Berserker",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=86, communication=80, leadership=75),
        nationality="Korea",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    c9.add_player(Player(
        name="Vulcan",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=88, leadership=85),
        nationality="Canada",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Cloud9 (NA)"] = c9
    
    # Team Liquid
    tl = Team(
        name="Team Liquid (NA)",
        region="NA",
        budget=13000000,
        fanbase=850000,
        championships=4,
        training_facilities=90,
        brand_value=12000000
    )
    
    tl.add_player(Player(
        name="Summit",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=87, communication=80, leadership=78),
        nationality="Korea",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="Pyosik",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=80),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="APA",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=83, leadership=75),
        nationality="United States",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    tl.add_player(Player(
        name="Yeon",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="United States",
        salary=420000,
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
        budget=11000000,
        fanbase=700000,
        championships=1,
        training_facilities=85,
        brand_value=9000000
    )
    
    eg.add_player(Player(
        name="Impact",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=89, communication=85, leadership=88),
        nationality="Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Inspired",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=88, communication=83, leadership=82),
        nationality="Poland",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="VicLa",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=80, leadership=75),
        nationality="Korea",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Kaori",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=80, leadership=75),
        nationality="Turkey",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    eg.add_player(Player(
        name="Vulcan",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=88, leadership=85),
        nationality="Canada",
        salary=480000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Evil Geniuses (NA)"] = eg

    # FlyQuest
    fly = Team(
        name="FlyQuest (NA)",
        region="NA",
        budget=9000000,
        fanbase=500000,
        championships=0,
        training_facilities=80,
        brand_value=7500000
    )
    
    fly.add_player(Player(
        name="Dhokla",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="United States",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Spica",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=85, leadership=83),
        nationality="United States",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Jensen",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=89, communication=85, leadership=82),
        nationality="Denmark",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Prince",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=80, leadership=75),
        nationality="Korea",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    fly.add_player(Player(
        name="Eyla",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=75),
        nationality="Australia",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["FlyQuest (NA)"] = fly

    # TSM
    tsm = Team(
        name="TSM (NA)",
        region="NA",
        budget=12000000,
        fanbase=1000000,
        championships=7,
        training_facilities=85,
        brand_value=13000000
    )
    
    tsm.add_player(Player(
        name="Huni",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=87, communication=83, leadership=80),
        nationality="Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="UmTi",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Ruby",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="China",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Tactical",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=75),
        nationality="United States",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    tsm.add_player(Player(
        name="Chime",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=81, leadership=75),
        nationality="United States",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["TSM (NA)"] = tsm

    # Golden Guardians
    gg = Team(
        name="Golden Guardians (NA)",
        region="NA",
        budget=8500000,
        fanbase=400000,
        championships=0,
        training_facilities=75,
        brand_value=6500000
    )
    
    gg.add_player(Player(
        name="Licorice",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=86, communication=84, leadership=82),
        nationality="United States",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="River",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=80, leadership=78),
        nationality="Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="Gori",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="Stixxay",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=83, leadership=80),
        nationality="United States",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    gg.add_player(Player(
        name="huhi",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=87, communication=85, leadership=82),
        nationality="Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Golden Guardians (NA)"] = gg

    # Dignitas
    dig = Team(
        name="Dignitas (NA)",
        region="NA",
        budget=8000000,
        fanbase=350000,
        championships=0,
        training_facilities=75,
        brand_value=6000000
    )
    
    dig.add_player(Player(
        name="FakeGod",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="United States",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="eXyu",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="United States",
        salary=330000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="Haeri",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="Australia",
        salary=330000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="Tomo",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="United States",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    dig.add_player(Player(
        name="IgNar",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=82, leadership=80),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Dignitas (NA)"] = dig

    # Immortals
    imt = Team(
        name="Immortals (NA)",
        region="NA",
        budget=8500000,
        fanbase=400000,
        championships=0,
        training_facilities=75,
        brand_value=6500000
    )
    
    imt.add_player(Player(
        name="Revenge",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="United States",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    imt.add_player(Player(
        name="Armao",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=83, communication=80, leadership=75),
        nationality="United States",
        salary=340000,
        contract_end=date(2024, 11, 21)
    ))
    
    imt.add_player(Player(
        name="Ablazeolive",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=81, leadership=75),
        nationality="Canada",
        salary=360000,
        contract_end=date(2024, 11, 21)
    ))
    
    imt.add_player(Player(
        name="WildTurtle",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=85, communication=83, leadership=82),
        nationality="Canada",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    imt.add_player(Player(
        name="Olleh",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=83, leadership=80),
        nationality="Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Immortals (NA)"] = imt

    # Counter Logic Gaming
    clg = Team(
        name="Counter Logic Gaming (NA)",
        region="NA",
        budget=9000000,
        fanbase=500000,
        championships=2,
        training_facilities=75,
        brand_value=7000000
    )
    
    clg.add_player(Player(
        name="Solo",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=85, communication=83, leadership=82),
        nationality="United States",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    clg.add_player(Player(
        name="Contractz",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=80),
        nationality="United States",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    clg.add_player(Player(
        name="Palafox",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=75),
        nationality="United States",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    clg.add_player(Player(
        name="Luger",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=75),
        nationality="Turkey",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    clg.add_player(Player(
        name="Poome",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=81, leadership=75),
        nationality="United States",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Counter Logic Gaming (NA)"] = clg

    # NRG
    nrg = Team(
        name="NRG (NA)",
        region="NA",
        budget=10000000,
        fanbase=600000,
        championships=0,
        training_facilities=80,
        brand_value=8000000
    )
    
    nrg.add_player(Player(
        name="Dhokla",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="United States",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="Svenskeren",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=87, communication=85, leadership=83),
        nationality="Denmark",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="Palafox",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=75),
        nationality="United States",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="FBI",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="Australia",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    nrg.add_player(Player(
        name="IgNar",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=86, communication=83, leadership=80),
        nationality="Korea",
        salary=420000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["NRG (NA)"] = nrg
    
    return teams
