-- Players table
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    nationality TEXT NOT NULL,
    mechanical_skill INTEGER NOT NULL CHECK (mechanical_skill BETWEEN 1 AND 100),
    game_knowledge INTEGER NOT NULL CHECK (game_knowledge BETWEEN 1 AND 100),
    communication INTEGER NOT NULL CHECK (communication BETWEEN 1 AND 100),
    leadership INTEGER NOT NULL CHECK (leadership BETWEEN 1 AND 100),
    salary INTEGER NOT NULL,
    contract_end DATE NOT NULL,
    team_id INTEGER,
    games_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    budget INTEGER NOT NULL,
    games_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    championship_points INTEGER DEFAULT 0
);

-- Matches table
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    winner_id INTEGER NOT NULL,
    team1_score INTEGER NOT NULL,
    team2_score INTEGER NOT NULL,
    match_date DATETIME NOT NULL,
    league_id INTEGER,
    FOREIGN KEY (team1_id) REFERENCES teams(id),
    FOREIGN KEY (team2_id) REFERENCES teams(id),
    FOREIGN KEY (winner_id) REFERENCES teams(id),
    FOREIGN KEY (league_id) REFERENCES leagues(id)
);

-- Leagues table
CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    season_start DATE,
    season_end DATE,
    current_week INTEGER DEFAULT 0,
    season_started BOOLEAN DEFAULT FALSE
);

-- League Teams (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS league_teams (
    league_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY (league_id, team_id),
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
