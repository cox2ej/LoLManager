from datetime import date
from src.models.team import Team
from src.models.player import Player, Role, PlayerStats
from src.models.league import League, Division

def create_lpl_league() -> League:
    """Create and return the LPL league with all teams."""
    # Create teams
    teams = create_lpl_teams()
    
    # Create divisions dictionary
    divisions = {
        "Regular Season": list(teams.values())
    }
    
    # Create and return the league
    return League("LPL", divisions)

def create_lpl_teams() -> dict[str, Team]:
    """Create and return a dictionary of LPL teams with their rosters."""
    teams = {}
    
    # JD Gaming
    jdg = Team(
        name="JD Gaming (CN)",
        region="CN",
        budget=14000000,
        fanbase=1800000,
        championships=3,
        training_facilities=95,
        brand_value=16000000
    )
    
    jdg.add_player(Player(
        name="369",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=88, communication=85, leadership=82),
        nationality="China",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    jdg.add_player(Player(
        name="Kanavi",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=91, game_knowledge=89, communication=85, leadership=83),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    jdg.add_player(Player(
        name="Knight",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=92, game_knowledge=90, communication=85, leadership=82),
        nationality="China",
        salary=900000,
        contract_end=date(2024, 11, 21)
    ))
    
    jdg.add_player(Player(
        name="Ruler",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=93, game_knowledge=90, communication=85, leadership=84),
        nationality="South Korea",
        salary=1000000,
        contract_end=date(2024, 11, 21)
    ))
    
    jdg.add_player(Player(
        name="Missing",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=85, leadership=82),
        nationality="China",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["JD Gaming (CN)"] = jdg

    # BLG
    blg = Team(
        name="Bilibili Gaming (CN)",
        region="CN",
        budget=12000000,
        fanbase=1200000,
        championships=1,
        training_facilities=90,
        brand_value=13000000
    )
    
    blg.add_player(Player(
        name="Bin",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=87, communication=83, leadership=80),
        nationality="China",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    blg.add_player(Player(
        name="Xun",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=82, leadership=78),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    blg.add_player(Player(
        name="Yagao",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=83, leadership=80),
        nationality="China",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    blg.add_player(Player(
        name="Elk",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=82, leadership=78),
        nationality="China",
        salary=550000,
        contract_end=date(2024, 11, 21)
    ))
    
    blg.add_player(Player(
        name="ON",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=79),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Bilibili Gaming (CN)"] = blg

    # LNG
    lng = Team(
        name="LNG Esports (CN)",
        region="CN",
        budget=11000000,
        fanbase=900000,
        championships=0,
        training_facilities=88,
        brand_value=11000000
    )
    
    lng.add_player(Player(
        name="Zika",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    lng.add_player(Player(
        name="Tarzan",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=89, communication=85, leadership=83),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    lng.add_player(Player(
        name="Scout",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=88, communication=84, leadership=81),
        nationality="South Korea",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    lng.add_player(Player(
        name="GALA",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=87, communication=83, leadership=80),
        nationality="China",
        salary=650000,
        contract_end=date(2024, 11, 21)
    ))
    
    lng.add_player(Player(
        name="Hang",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=79),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["LNG Esports (CN)"] = lng

    # EDward Gaming
    edg = Team(
        name="EDward Gaming (CN)",
        region="CN",
        budget=12000000,
        fanbase=1500000,
        championships=2,
        training_facilities=92,
        brand_value=14000000
    )
    
    edg.add_player(Player(
        name="Ale",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    edg.add_player(Player(
        name="JieJie",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=87, communication=84, leadership=82),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    edg.add_player(Player(
        name="FoFo",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="Taiwan",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    edg.add_player(Player(
        name="Leave",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=86, communication=83, leadership=80),
        nationality="China",
        salary=500000,
        contract_end=date(2024, 11, 21)
    ))
    
    edg.add_player(Player(
        name="Meiko",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=90, communication=88, leadership=90),
        nationality="China",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["EDward Gaming (CN)"] = edg

    # Top Esports
    tes = Team(
        name="Top Esports (CN)",
        region="CN",
        budget=13000000,
        fanbase=1600000,
        championships=1,
        training_facilities=93,
        brand_value=15000000
    )
    
    tes.add_player(Player(
        name="Qingtian",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    tes.add_player(Player(
        name="Tian",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=88, communication=85, leadership=83),
        nationality="China",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    tes.add_player(Player(
        name="Rookie",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=91, game_knowledge=90, communication=85, leadership=85),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    tes.add_player(Player(
        name="JackeyLove",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=91, game_knowledge=89, communication=85, leadership=83),
        nationality="China",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    tes.add_player(Player(
        name="Mark",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Top Esports (CN)"] = tes

    # RNG
    rng = Team(
        name="Royal Never Give Up (CN)",
        region="CN",
        budget=12500000,
        fanbase=1700000,
        championships=3,
        training_facilities=92,
        brand_value=14500000
    )
    
    rng.add_player(Player(
        name="Breathe",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    rng.add_player(Player(
        name="XLB",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    rng.add_player(Player(
        name="Xiaohu",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=91, communication=88, leadership=90),
        nationality="China",
        salary=900000,
        contract_end=date(2024, 11, 21)
    ))
    
    rng.add_player(Player(
        name="Betty",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="Taiwan",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    rng.add_player(Player(
        name="Ming",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=89, game_knowledge=90, communication=88, leadership=88),
        nationality="China",
        salary=700000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Royal Never Give Up (CN)"] = rng

    # WE
    we = Team(
        name="Team WE (CN)",
        region="CN",
        budget=9000000,
        fanbase=800000,
        championships=1,
        training_facilities=85,
        brand_value=9000000
    )
    
    we.add_player(Player(
        name="Biubiu",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=80, leadership=75),
        nationality="China",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    we.add_player(Player(
        name="Heng",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=83, game_knowledge=82, communication=80, leadership=75),
        nationality="China",
        salary=300000,
        contract_end=date(2024, 11, 21)
    ))
    
    we.add_player(Player(
        name="Shanks",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="China",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    we.add_player(Player(
        name="Hope",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=82, leadership=78),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    we.add_player(Player(
        name="Crisp",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=84, leadership=82),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Team WE (CN)"] = we

    # FunPlus Phoenix
    fpx = Team(
        name="FunPlus Phoenix (CN)",
        region="CN",
        budget=11000000,
        fanbase=1000000,
        championships=1,
        training_facilities=88,
        brand_value=12000000
    )
    
    fpx.add_player(Player(
        name="fearness",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="China",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    fpx.add_player(Player(
        name="H4cker",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    fpx.add_player(Player(
        name="Care",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    fpx.add_player(Player(
        name="Lwx",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    fpx.add_player(Player(
        name="Lele",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=78),
        nationality="China",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["FunPlus Phoenix (CN)"] = fpx

    # OMG
    omg = Team(
        name="Oh My God (CN)",
        region="CN",
        budget=9500000,
        fanbase=700000,
        championships=0,
        training_facilities=85,
        brand_value=9000000
    )
    
    omg.add_player(Player(
        name="shanji",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="China",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    omg.add_player(Player(
        name="Aki",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=78),
        nationality="China",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    omg.add_player(Player(
        name="Creme",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=86, game_knowledge=85, communication=83, leadership=80),
        nationality="China",
        salary=400000,
        contract_end=date(2024, 11, 21)
    ))
    
    omg.add_player(Player(
        name="Able",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=85, game_knowledge=84, communication=82, leadership=78),
        nationality="China",
        salary=350000,
        contract_end=date(2024, 11, 21)
    ))
    
    omg.add_player(Player(
        name="ppgod",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=84, game_knowledge=83, communication=82, leadership=78),
        nationality="China",
        salary=320000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Oh My God (CN)"] = omg

    # Weibo Gaming
    weibo = Team(
        name="Weibo Gaming (CN)",
        region="CN",
        budget=10500000,
        fanbase=900000,
        championships=0,
        training_facilities=87,
        brand_value=11000000
    )
    
    weibo.add_player(Player(
        name="TheShy",
        role=Role.TOP,
        stats=PlayerStats(mechanical_skill=91, game_knowledge=89, communication=83, leadership=82),
        nationality="South Korea",
        salary=800000,
        contract_end=date(2024, 11, 21)
    ))
    
    weibo.add_player(Player(
        name="Karsa",
        role=Role.JUNGLE,
        stats=PlayerStats(mechanical_skill=88, game_knowledge=89, communication=85, leadership=85),
        nationality="Taiwan",
        salary=600000,
        contract_end=date(2024, 11, 21)
    ))
    
    weibo.add_player(Player(
        name="Xiaohu",
        role=Role.MID,
        stats=PlayerStats(mechanical_skill=90, game_knowledge=91, communication=88, leadership=90),
        nationality="China",
        salary=900000,
        contract_end=date(2024, 11, 21)
    ))
    
    weibo.add_player(Player(
        name="Light",
        role=Role.ADC,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=83, leadership=80),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    weibo.add_player(Player(
        name="Crisp",
        role=Role.SUPPORT,
        stats=PlayerStats(mechanical_skill=87, game_knowledge=86, communication=84, leadership=82),
        nationality="China",
        salary=450000,
        contract_end=date(2024, 11, 21)
    ))
    
    teams["Weibo Gaming (CN)"] = weibo

    return teams
