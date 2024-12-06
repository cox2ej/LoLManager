import pytest
from datetime import datetime, date, timedelta
from src.models.player import Player, PlayerStats, Role
from src.models.team import Team
from src.models.match import Match


@pytest.fixture
def sample_teams():
    # Create two teams with different strength levels
    team1 = Team("T1", "LCK", 1000000, 1)
    team2 = Team("GenG", "LCK", 1000000, 2)
    
    contract_end = date.today() + timedelta(days=365)
    
    # Create players for team1 (stronger)
    for role in Role:
        stats = PlayerStats(
            mechanical_skill=90,
            game_knowledge=85,
            communication=80,
            leadership=75
        )
        player = Player(
            name=f"T1_{role.value}",
            role=role,
            stats=stats,
            nationality="South Korea",
            salary=100000,
            contract_end=contract_end
        )
        team1.add_player(player)
    
    # Create players for team2 (weaker)
    for role in Role:
        stats = PlayerStats(
            mechanical_skill=80,
            game_knowledge=75,
            communication=70,
            leadership=65
        )
        player = Player(
            name=f"GenG_{role.value}",
            role=role,
            stats=stats,
            nationality="South Korea",
            salary=100000,
            contract_end=contract_end
        )
        team2.add_player(player)
    
    return team1, team2


@pytest.fixture
def sample_match(sample_teams):
    team1, team2 = sample_teams
    return Match(team1, team2, datetime.now())


def test_match_creation(sample_match):
    assert sample_match.result is None
    assert isinstance(sample_match.match_date, datetime)


def test_match_simulation(sample_match):
    result = sample_match.simulate()
    
    # Check if result was created
    assert result is not None
    assert result.winner in [sample_match.team1, sample_match.team2]
    assert result.loser in [sample_match.team1, sample_match.team2]
    assert result.winner != result.loser
    
    # Check scores
    assert result.winner_score == 2  # Best of 3
    assert result.loser_score in [0, 1]
    
    # Check if teams were updated
    total_games = result.winner_score + result.loser_score
    assert result.winner.wins == result.winner_score
    assert result.loser.losses == result.winner_score  # Loser's losses should equal winner's wins
    assert result.winner.losses == result.loser_score
    assert result.loser.wins == result.loser_score


def test_invalid_match_simulation(sample_teams):
    team1, team2 = sample_teams
    
    # Remove all players from team1
    for role in Role:
        players = team1.roster[role].copy()
        for player in players:
            team1.remove_player(player)
    
    match = Match(team1, team2, datetime.now())
    
    # Should raise error when trying to simulate with invalid roster
    with pytest.raises(ValueError):
        match.simulate()


def test_match_string_representation(sample_match):
    # Before simulation
    expected_str = f"{sample_match.team1.name} vs {sample_match.team2.name} - {sample_match.match_date}"
    assert str(sample_match) == expected_str
    
    # After simulation
    result = sample_match.simulate()
    expected_str = f"{result.winner.name} defeated {result.loser.name} {result.winner_score}-{result.loser_score}"
    assert str(sample_match) == expected_str
