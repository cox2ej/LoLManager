import os
import pytest
from datetime import date, datetime, timedelta
from pathlib import Path

from src.database.db_manager import DatabaseManager
from src.models.player import Player, PlayerStats, Role
from src.models.team import Team
from src.models.match import Match, MatchResult
from src.models.league import League

@pytest.fixture
def db_manager():
    """Create a test database manager."""
    test_db_path = "data/test.db"
    
    # Remove test database if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = DatabaseManager(test_db_path)
    yield db
    
    # Cleanup
    db.close()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.fixture
def sample_player():
    """Create a sample player for testing."""
    stats = PlayerStats(
        mechanical_skill=85,
        game_knowledge=90,
        communication=75,
        leadership=80
    )
    return Player(
        name="Test Player",
        role=Role.MID,
        stats=stats,
        nationality="USA",
        salary=100000,
        contract_end=date.today() + timedelta(days=365)
    )

@pytest.fixture
def sample_team():
    """Create a sample team for testing."""
    return Team(
        name="Test Team",
        region="NA",
        budget=1000000
    )

def test_player_save_load(db_manager, sample_player):
    """Test saving and loading a player."""
    # Save player
    player_id = db_manager.save_player(sample_player)
    assert player_id is not None
    
    # Load player
    loaded_player = db_manager.load_player(player_id)
    assert loaded_player is not None
    assert loaded_player.name == sample_player.name
    assert loaded_player.role == sample_player.role
    assert loaded_player.nationality == sample_player.nationality
    assert loaded_player.salary == sample_player.salary
    assert loaded_player.contract_end == sample_player.contract_end
    assert loaded_player.stats.mechanical_skill == sample_player.stats.mechanical_skill
    assert loaded_player.stats.game_knowledge == sample_player.stats.game_knowledge
    assert loaded_player.stats.communication == sample_player.stats.communication
    assert loaded_player.stats.leadership == sample_player.stats.leadership

def test_team_save_load(db_manager, sample_team, sample_player):
    """Test saving and loading a team with players."""
    # Add player to team
    sample_team.add_player(sample_player)
    
    # Save team
    team_id = db_manager.save_team(sample_team)
    sample_team.team_id = team_id
    assert team_id is not None
    
    # Load team
    loaded_team = db_manager.load_team(team_id)
    assert loaded_team is not None
    assert loaded_team.name == sample_team.name
    assert loaded_team.region == sample_team.region
    assert loaded_team.budget == sample_team.budget
    assert len(loaded_team.roster[Role.MID]) == 1
    
    # Check player data
    loaded_player = loaded_team.roster[Role.MID][0]
    assert loaded_player.name == sample_player.name
    assert loaded_player.role == sample_player.role

def test_match_save_load(db_manager, sample_team):
    """Test saving and loading a match."""
    # Create two teams
    team1 = sample_team
    team2 = Team("Test Team 2", "EU", 1000000)
    
    # Save teams
    team1.team_id = db_manager.save_team(team1)
    team2.team_id = db_manager.save_team(team2)
    
    # Create and save match
    match_date = datetime.now()
    match = Match(team1, team2, match_date)
    match.result = MatchResult(team1, team2, 2, 1, match_date)
    
    match_id = db_manager.save_match(match)
    assert match_id is not None
    
    # Load match
    loaded_match = db_manager.load_match(match_id)
    assert loaded_match is not None
    assert loaded_match.team1.name == team1.name
    assert loaded_match.team2.name == team2.name
    assert loaded_match.result.winner.name == team1.name
    assert loaded_match.result.winner_score == 2
    assert loaded_match.result.loser_score == 1

def test_league_save_load(db_manager, sample_team):
    """Test saving and loading a league."""
    # Create teams
    teams = [
        sample_team,
        Team("Test Team 2", "EU", 1000000),
        Team("Test Team 3", "KR", 1000000),
        Team("Test Team 4", "CN", 1000000)
    ]
    
    # Save teams
    for team in teams:
        team.team_id = db_manager.save_team(team)
    
    # Create and save league
    league = League("Test League", teams)
    league_id = db_manager.save_league(league)
    assert league_id is not None
    
    # Load league
    loaded_league = db_manager.load_league(league_id)
    assert loaded_league is not None
    assert loaded_league.name == league.name
    assert len(loaded_league.teams) == len(teams)
    assert loaded_league.teams[0].name == teams[0].name
