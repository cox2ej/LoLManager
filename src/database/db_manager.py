import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from src.models.player import Player, PlayerStats, Role
from src.models.team import Team
from src.models.match import Match, MatchResult
from src.models.league import League


class DatabaseManager:
    def __init__(self, db_path: str = "data/game.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create tables
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables from schema.sql."""
        with open("src/database/schema.sql", "r") as f:
            schema = f.read()
            self.conn.executescript(schema)
            self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    # Player operations
    def save_player(self, player: Player) -> int:
        """Save player to database. Return player ID."""
        cursor = self.conn.cursor()
        
        query = """
        INSERT INTO players (
            name, role, nationality, mechanical_skill, game_knowledge,
            communication, leadership, salary, contract_end, team_id,
            games_played, wins, losses
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            player.name,
            player.role.value,
            player.nationality,
            player.stats.mechanical_skill,
            player.stats.game_knowledge,
            player.stats.communication,
            player.stats.leadership,
            player.salary,
            player.contract_end.isoformat(),
            player.team_id,
            player.games_played,
            player.wins,
            player.losses
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def load_player(self, player_id: int) -> Optional[Player]:
        """Load player from database by ID."""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM players WHERE id = ?"
        cursor.execute(query, (player_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        stats = PlayerStats(
            mechanical_skill=row['mechanical_skill'],
            game_knowledge=row['game_knowledge'],
            communication=row['communication'],
            leadership=row['leadership']
        )
        
        player = Player(
            name=row['name'],
            role=Role[row['role'].upper()],
            stats=stats,
            nationality=row['nationality'],
            salary=row['salary'],
            contract_end=date.fromisoformat(row['contract_end']),
            team_id=row['team_id']
        )
        
        player.games_played = row['games_played']
        player.wins = row['wins']
        player.losses = row['losses']
        
        return player
    
    # Team operations
    def save_team(self, team: Team) -> int:
        """Save team to database. Return team ID."""
        cursor = self.conn.cursor()
        
        query = """
        INSERT INTO teams (
            name, region, budget, games_played, wins,
            losses, championship_points
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            team.name,
            team.region,
            team.budget,
            team.wins + team.losses,  # games_played
            team.wins,
            team.losses,
            team.championship_points
        ))
        
        team_id = cursor.lastrowid
        
        # Save all players in roster
        for role_players in team.roster.values():
            for player in role_players:
                player.team_id = team_id
                self.save_player(player)
        
        self.conn.commit()
        return team_id
    
    def load_team(self, team_id: int) -> Optional[Team]:
        """Load team and its roster from database by ID."""
        cursor = self.conn.cursor()
        
        # Load team data
        query = "SELECT * FROM teams WHERE id = ?"
        cursor.execute(query, (team_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        team = Team(
            name=row['name'],
            region=row['region'],
            budget=row['budget'],
            team_id=team_id
        )
        
        team.wins = row['wins']
        team.losses = row['losses']
        team.championship_points = row['championship_points']
        
        # Load team's players
        query = "SELECT id FROM players WHERE team_id = ?"
        cursor.execute(query, (team_id,))
        
        for player_row in cursor.fetchall():
            player = self.load_player(player_row['id'])
            if player:
                team.add_player(player)
        
        return team
    
    # Match operations
    def save_match(self, match: Match) -> int:
        """Save match to database. Return match ID."""
        if not match.result:
            raise ValueError("Cannot save match without result")
        
        cursor = self.conn.cursor()
        
        query = """
        INSERT INTO matches (
            team1_id, team2_id, winner_id, team1_score,
            team2_score, match_date, league_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        result = match.result
        team1_score = result.winner_score if result.winner == match.team1 else result.loser_score
        team2_score = result.winner_score if result.winner == match.team2 else result.loser_score
        
        cursor.execute(query, (
            match.team1.team_id,
            match.team2.team_id,
            result.winner.team_id,
            team1_score,
            team2_score,
            match.match_date.isoformat(),
            None  # league_id will be set when leagues are implemented
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def load_match(self, match_id: int) -> Optional[Match]:
        """Load match from database by ID."""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM matches WHERE id = ?"
        cursor.execute(query, (match_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        team1 = self.load_team(row['team1_id'])
        team2 = self.load_team(row['team2_id'])
        
        if not team1 or not team2:
            return None
        
        match = Match(
            team1=team1,
            team2=team2,
            match_date=datetime.fromisoformat(row['match_date'])
        )
        
        # Create match result
        winner = team1 if row['winner_id'] == team1.team_id else team2
        loser = team2 if winner == team1 else team1
        winner_score = max(row['team1_score'], row['team2_score'])
        loser_score = min(row['team1_score'], row['team2_score'])
        
        match.result = MatchResult(
            winner=winner,
            loser=loser,
            winner_score=winner_score,
            loser_score=loser_score,
            match_date=match.match_date
        )
        
        return match
    
    # League operations
    def save_league(self, league: League) -> int:
        """Save league to database. Return league ID."""
        cursor = self.conn.cursor()
        
        # Save league data
        query = """
        INSERT INTO leagues (
            name, season_start, season_end,
            current_week, season_started
        ) VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            league.name,
            None,  # season_start (will be set when season starts)
            None,  # season_end
            league.current_week,
            league.season_started
        ))
        
        league_id = cursor.lastrowid
        
        # Save league teams
        for team in league.teams:
            # Skip saving team if it's already in the database
            if not hasattr(team, 'team_id'):
                team.team_id = self.save_team(team)
            
            cursor.execute(
                "INSERT INTO league_teams (league_id, team_id) VALUES (?, ?)",
                (league_id, team.team_id)
            )
        
        self.conn.commit()
        return league_id
    
    def load_league(self, league_id: int) -> Optional[League]:
        """Load league from database by ID."""
        cursor = self.conn.cursor()
        
        # Load league data
        query = "SELECT * FROM leagues WHERE id = ?"
        cursor.execute(query, (league_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Load league teams
        query = """
        SELECT team_id FROM league_teams
        WHERE league_id = ?
        """
        cursor.execute(query, (league_id,))
        
        teams = []
        for team_row in cursor.fetchall():
            team = self.load_team(team_row['team_id'])
            if team:
                teams.append(team)
        
        if not teams:
            return None
        
        league = League(row['name'], teams)
        league.current_week = row['current_week']
        league.season_started = bool(row['season_started'])
        
        return league
