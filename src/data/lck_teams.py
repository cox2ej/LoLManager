from datetime import date
from src.models.team import Team
from src.models.player import Player, Role, PlayerStats
from src.models.league import League, Division

def create_lck_league() -> League:
    """Create and return the LCK league with all teams."""
    # Create teams
    teams = create_lck_teams()
    
    # Create divisions dictionary
    divisions = {
        "Regular Season": list(teams.values())
    }
    
    # Create and return the league
    return League("LCK", divisions)

def create_lck_teams() -> dict[str, Team]:
    """Create and return a dictionary of LCK teams with their rosters."""
    teams = {}
    
    # T1
    t1 = Team(
        name="T1 (KR)",
        region="KR",
        budget=15000000,
        fanbase=2000000,
        championships=10,
        training_facilities=98,
        brand_value=20000000
    )
    
    t1.add_player(Player(
        name="Zeus",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=85, leadership=83),
        nationality="South Korea",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    t1.add_player(Player(
        name="Oner",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=89, communication=85, leadership=82),
        nationality="South Korea",
        salary=650000,
        contract_end=date(2024, 11, 21)
    ))
    
    t1.add_player(Player(
        name="Faker",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=95, game_knowledge=95, communication=90, leadership=95),
        nationality="South Korea",
        salary=2000000,
        contract_end=date(2024, 11, 21)
    ))
    
    t1.add_player(Player(
        name="Gumayusi",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=91, game_knowledge=88, communication=85, leadership=80),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    t1.add_player(Player(
        name="Keria",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=88, leadership=85),
        nationality="South Korea",
        salary=750000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["T1 (KR)"] = t1

    # Gen.G
    geng = Team(
        name="Gen.G (KR)",
        region="KR",
        budget=13000000,
        fanbase=1500000,
        championships=4,
        training_facilities=95,
        brand_value=15000000
    )
    
    geng.add_player(Player(
        name="Doran",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    geng.add_player(Player(
        name="Canyon",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=85, leadership=83),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    geng.add_player(Player(
        name="Chovy",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=93, game_knowledge=91, communication=85, leadership=82),
        nationality="South Korea",
        salary=900000,
        contract_end=date(2024, 11, 21)
    ))
    
    geng.add_player(Player(
        name="Peyz",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=85, communication=82, leadership=78),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    geng.add_player(Player(
        name="Delight",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=78),
        nationality="South Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Gen.G (KR)"] = geng

    # KT Rolster
    kt = Team(
        name="KT Rolster (KR)",
        region="KR",
        budget=11000000,
        fanbase=900000,
        championships=2,
        training_facilities=90,
        brand_value=12000000
    )
    
    kt.add_player(Player(
        name="Kiin",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=83, leadership=80),
        nationality="South Korea",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    kt.add_player(Player(
        name="Cuzz",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="South Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    kt.add_player(Player(
        name="Bdd",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    kt.add_player(Player(
        name="Aiming",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=82, leadership=78),
        nationality="South Korea",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    kt.add_player(Player(
        name="Lehends",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=84, leadership=80),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["KT Rolster (KR)"] = kt

    # Dplus KIA
    dplus = Team(
        name="Dplus KIA (KR)",
        region="KR",
        budget=10000000,
        fanbase=700000,
        championships=1,
        training_facilities=88,
        brand_value=11000000
    )
    
    dplus.add_player(Player(
        name="Kingen",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="South Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    dplus.add_player(Player(
        name="Lucid",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    dplus.add_player(Player(
        name="ShowMaker",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=91, communication=85, leadership=85),
        nationality="South Korea",
        salary=900000,
        contract_end=date(2024, 11, 21)
    ))
    
    dplus.add_player(Player(
        name="Aiming",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=83, leadership=80),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    dplus.add_player(Player(
        name="Kellin",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=83, leadership=78),
        nationality="South Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Dplus KIA (KR)"] = dplus

    # Hanwha Life Esports
    hle = Team(
        name="Hanwha Life Esports (KR)",
        region="KR",
        budget=9500000,
        fanbase=600000,
        championships=0,
        training_facilities=85,
        brand_value=9000000
    )
    
    hle.add_player(Player(
        name="DuDu",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=380000,
        contract_end=date(2024, 11, 21)
    ))
    
    hle.add_player(Player(
        name="Peanut",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=89, communication=85, leadership=85),
        nationality="South Korea",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    hle.add_player(Player(
        name="Zeka",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="South Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    hle.add_player(Player(
        name="Viper",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=88, communication=85, leadership=82),
        nationality="South Korea",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    hle.add_player(Player(
        name="Life",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Hanwha Life Esports (KR)"] = hle

    # Nongshim RedForce
    ns = Team(
        name="Nongshim RedForce (KR)",
        region="KR",
        budget=8500000,
        fanbase=400000,
        championships=0,
        training_facilities=82,
        brand_value=8000000
    )
    
    ns.add_player(Player(
        name="DnDn",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    ns.add_player(Player(
        name="Sylvie",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    ns.add_player(Player(
        name="FIESTA",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    ns.add_player(Player(
        name="vital",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    ns.add_player(Player(
        name="Peter",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Nongshim RedForce (KR)"] = ns

    # Kwangdong Freecs
    kdf = Team(
        name="Kwangdong Freecs (KR)",
        region="KR",
        budget=8000000,
        fanbase=350000,
        championships=0,
        training_facilities=80,
        brand_value=7500000
    )
    
    kdf.add_player(Player(
        name="Dudu",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    kdf.add_player(Player(
        name="YoungJae",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    kdf.add_player(Player(
        name="BuLLDoG",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    kdf.add_player(Player(
        name="Taeyoon",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    kdf.add_player(Player(
        name="Jun",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=82, game_knowledge=81, communication=80, leadership=75),
        nationality="South Korea",
        salary=280000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Kwangdong Freecs (KR)"] = kdf

    # BRION
    brion = Team(
        name="BRION (KR)",
        region="KR",
        budget=7500000,
        fanbase=300000,
        championships=0,
        training_facilities=75,
        brand_value=6500000
    )
    
    brion.add_player(Player(
        name="Morgan",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    brion.add_player(Player(
        name="UmTi",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    brion.add_player(Player(
        name="Karis",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    brion.add_player(Player(
        name="Envyy",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    brion.add_player(Player(
        name="Effort",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["BRION (KR)"] = brion

    # DRX
    drx = Team(
        name="DRX (KR)",
        region="KR",
        budget=9000000,
        fanbase=550000,
        championships=1,
        training_facilities=85,
        brand_value=9500000
    )
    
    drx.add_player(Player(
        name="Rascal",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    drx.add_player(Player(
        name="Canyon",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=85, leadership=83),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    drx.add_player(Player(
        name="Fate",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    drx.add_player(Player(
        name="Teddy",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="South Korea",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    drx.add_player(Player(
        name="BeryL",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=88, communication=85, leadership=83),
        nationality="South Korea",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["DRX (KR)"] = drx

    # Liiv SANDBOX
    lsb = Team(
        name="Liiv SANDBOX (KR)",
        region="KR",
        budget=8000000,
        fanbase=350000,
        championships=0,
        training_facilities=80,
        brand_value=7500000
    )
    
    lsb.add_player(Player(
        name="Clear",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    lsb.add_player(Player(
        name="Willer",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="South Korea",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    lsb.add_player(Player(
        name="Clozer",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="South Korea",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    lsb.add_player(Player(
        name="Envyy",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="South Korea",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    lsb.add_player(Player(
        name="Kael",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="South Korea",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Liiv SANDBOX (KR)"] = lsb

    return teams
