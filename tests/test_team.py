import pytest
from datetime import date, timedelta
from src.models.player import Player, PlayerStats, Role
from src.models.team import Team


@pytest.fixture
def sample_team():
    return Team(
        name="T1",
        region="LCK",
        budget=1000000,
        team_id=1
    )


@pytest.fixture
def sample_players():
    contract_end = date.today() + timedelta(days=365)
    players = []
    
    # Create one player for each role
    roles_data = [
        ("Zeus", Role.TOP, 85),
        ("Oner", Role.JUNGLE, 88),
        ("Faker", Role.MID, 90),
        ("Gumayusi", Role.ADC, 87),
        ("Keria", Role.SUPPORT, 89)
    ]
    
    for name, role, skill in roles_data:
        stats = PlayerStats(
            mechanical_skill=skill,
            game_knowledge=skill-5,
            communication=skill-10,
            leadership=skill-15
        )
        
        player = Player(
            name=name,
            role=role,
            stats=stats,
            nationality="South Korea",
            salary=100000,
            contract_end=contract_end
        )
        players.append(player)
    
    return players


def test_team_creation(sample_team):
    assert sample_team.name == "T1"
    assert sample_team.region == "LCK"
    assert sample_team.budget == 1000000
    assert sample_team.team_id == 1
    assert sample_team.wins == 0
    assert sample_team.losses == 0


def test_roster_management(sample_team, sample_players):
    # Add all players to team
    for player in sample_players:
        sample_team.add_player(player)
    
    # Check if roster is valid
    assert sample_team.is_roster_valid()
    
    # Check if each role has exactly one player
    for role in Role:
        assert len(sample_team.roster[role]) == 1
    
    # Remove a player
    sample_team.remove_player(sample_players[0])
    assert not sample_team.is_roster_valid()  # Missing TOP
    assert sample_players[0].team_id is None


def test_starting_lineup(sample_team, sample_players):
    # Add all players to team
    for player in sample_players:
        sample_team.add_player(player)
    
    lineup = sample_team.get_starting_lineup()
    
    # Check if all roles are filled
    assert all(lineup.values())
    
    # Check if players are in correct roles
    for role, player in lineup.items():
        assert player.role == role


def test_team_salary(sample_team, sample_players):
    # Add all players to team
    for player in sample_players:
        sample_team.add_player(player)
    
    expected_total = len(sample_players) * 100000
    assert sample_team.get_total_salary() == expected_total


def test_team_performance(sample_team, sample_players):
    # Add all players to team
    for player in sample_players:
        sample_team.add_player(player)
    
    # Simulate some wins and losses
    sample_team.update_performance(True)
    sample_team.update_performance(True)
    sample_team.update_performance(False)
    
    assert sample_team.wins == 2
    assert sample_team.losses == 1
    assert sample_team.win_rate == (2/3) * 100
    
    # Check if players' stats were updated
    lineup = sample_team.get_starting_lineup()
    for player in lineup.values():
        assert player.games_played == 3
        assert player.wins == 2
        assert player.losses == 1


def test_roster_strength(sample_team, sample_players):
    # Add all players to team
    for player in sample_players:
        sample_team.add_player(player)
    
    strength = sample_team.get_roster_strength()
    assert 0 <= strength <= 100  # Should be within valid range
    
    # Remove all players
    for player in sample_players:
        sample_team.remove_player(player)
    
    assert sample_team.get_roster_strength() == 0  # No players = 0 strength
