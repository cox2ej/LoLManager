import pytest
from datetime import datetime, date, timedelta
from src.models.player import Player, PlayerStats, Role
from src.models.team import Team
from src.models.league import League


@pytest.fixture
def sample_teams():
    teams = []
    team_data = [
        ("T1", 90),
        ("GenG", 85),
        ("DRX", 80),
        ("KT", 75)
    ]
    
    for team_name, base_skill in team_data:
        team = Team(team_name, "LCK", 1000000, len(teams) + 1)
        
        # Add players to team
        contract_end = date.today() + timedelta(days=365)
        for role in Role:
            stats = PlayerStats(
                mechanical_skill=base_skill,
                game_knowledge=base_skill-5,
                communication=base_skill-10,
                leadership=base_skill-15
            )
            player = Player(
                name=f"{team_name}_{role.value}",
                role=role,
                stats=stats,
                nationality="South Korea",
                salary=100000,
                contract_end=contract_end
            )
            team.add_player(player)
        
        teams.append(team)
    
    return teams


@pytest.fixture
def sample_league(sample_teams):
    return League("LCK Spring Split", sample_teams)


def test_league_creation(sample_league):
    assert sample_league.name == "LCK Spring Split"
    assert len(sample_league.teams) == 4
    assert not sample_league.season_started
    assert sample_league.current_week == 0


def test_schedule_generation(sample_league):
    start_date = datetime.now()
    matches = sample_league.generate_schedule(start_date)
    
    # Each team plays against every other team twice
    expected_matches = len(sample_league.teams) * (len(sample_league.teams) - 1)
    assert len(matches) == expected_matches
    
    # Check if all teams play equal number of matches
    team_matches = {team: 0 for team in sample_league.teams}
    for match in matches:
        team_matches[match.team1] += 1
        team_matches[match.team2] += 1
    
    # Each team should play against every other team twice
    expected_per_team = (len(sample_league.teams) - 1) * 2
    assert all(count == expected_per_team for count in team_matches.values())


def test_season_simulation(sample_league):
    start_date = datetime.now()
    sample_league.start_season(start_date)
    
    assert sample_league.season_started
    assert sample_league.current_week == 0
    
    # Simulate entire season
    while not sample_league.is_season_finished():
        results = sample_league.simulate_week()
        assert len(results) > 0  # Should have some matches each week


def test_standings_calculation(sample_league):
    start_date = datetime.now()
    sample_league.start_season(start_date)
    
    # Simulate a few weeks
    for _ in range(3):
        sample_league.simulate_week()
    
    standings = sample_league.get_standings()
    
    # Check if standings are properly sorted
    for i in range(len(standings) - 1):
        current = standings[i]
        next_team = standings[i + 1]
        assert (current['wins'] > next_team['wins'] or 
                (current['wins'] == next_team['wins'] and 
                 current['win_rate'] >= next_team['win_rate']))


def test_invalid_league_creation():
    # Should raise error with less than 4 teams
    teams = [Team(f"Team{i}", "LCK", 1000000, i) for i in range(3)]
    with pytest.raises(ValueError):
        League("Invalid League", teams)


def test_champion_determination(sample_league):
    start_date = datetime.now()
    sample_league.start_season(start_date)
    
    # No champion before season end
    assert sample_league.get_champion() is None
    
    # Simulate entire season
    while not sample_league.is_season_finished():
        sample_league.simulate_week()
    
    # Should have a champion after season ends
    champion = sample_league.get_champion()
    assert champion is not None
    assert champion in sample_league.teams
