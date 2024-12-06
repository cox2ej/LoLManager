import pytest
from datetime import date, timedelta
from src.models.player import Player, PlayerStats, Role


@pytest.fixture
def sample_stats():
    return PlayerStats(
        mechanical_skill=85,
        game_knowledge=80,
        communication=75,
        leadership=70
    )


@pytest.fixture
def sample_player(sample_stats):
    return Player(
        name="Faker",
        role=Role.MID,
        stats=sample_stats,
        nationality="South Korea",
        salary=100000,
        contract_end=date.today() + timedelta(days=365)
    )


def test_player_creation(sample_player):
    assert sample_player.name == "Faker"
    assert sample_player.role == Role.MID
    assert sample_player.nationality == "South Korea"
    assert sample_player.salary == 100000
    assert sample_player.games_played == 0
    assert sample_player.wins == 0
    assert sample_player.losses == 0


def test_player_stats_overall_rating(sample_stats):
    # Expected rating based on weights:
    # (85 * 0.35) + (80 * 0.35) + (75 * 0.15) + (70 * 0.15) = 79.5
    expected_rating = 79.5
    assert sample_stats.overall_rating == expected_rating


def test_player_win_rate(sample_player):
    # Initial win rate should be 0
    assert sample_player.win_rate == 0.0
    
    # After 2 wins and 1 loss
    sample_player.update_performance(True)
    sample_player.update_performance(True)
    sample_player.update_performance(False)
    
    assert sample_player.games_played == 3
    assert sample_player.wins == 2
    assert sample_player.losses == 1
    assert sample_player.win_rate == (2/3) * 100  # 66.67%


def test_contract_expiration(sample_player):
    today = date.today()
    
    # Contract should not be expired
    assert not sample_player.is_contract_expired(today)
    
    # Contract should be expired after end date
    future_date = today + timedelta(days=366)
    assert sample_player.is_contract_expired(future_date)


def test_player_string_representation(sample_player):
    expected_str = "Faker (Mid) - Rating: 79.5 - Win Rate: 0.0%"
    assert str(sample_player) == expected_str
