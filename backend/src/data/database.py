"""
SQLite database connection, schema management, and CRUD operations.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from ..config import DB_PATH


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS teams (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    "group" TEXT NOT NULL,
    fifa_rank INTEGER DEFAULT 0,
    elo_rating REAL DEFAULT 1500.0,
    confederation TEXT DEFAULT '',
    market_value REAL
);

CREATE TABLE IF NOT EXISTS matches (
    id TEXT PRIMARY KEY,
    home_team_id TEXT NOT NULL,
    away_team_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    "group" TEXT,
    match_date TEXT,
    venue TEXT,
    city TEXT,
    home_score INTEGER,
    away_score INTEGER,
    status TEXT DEFAULT 'scheduled',
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id)
);

CREATE TABLE IF NOT EXISTS team_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id TEXT NOT NULL,
    rating_date TEXT NOT NULL,
    elo_rating REAL NOT NULL,
    fifa_rank INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    home_team_id TEXT NOT NULL,
    away_team_id TEXT NOT NULL,
    home_win_prob REAL,
    draw_prob REAL,
    away_win_prob REAL,
    predicted_home_goals REAL,
    predicted_away_goals REAL,
    elo_home_win_prob REAL,
    poisson_home_win_prob REAL,
    lightgbm_home_win_prob REAL,
    llm_correction REAL,
    llm_narrative TEXT,
    model_version TEXT DEFAULT '1.0.0',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (match_id) REFERENCES matches(id)
);

CREATE TABLE IF NOT EXISTS tournament_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id TEXT NOT NULL,
    champion_prob REAL,
    final_prob REAL,
    semi_final_prob REAL,
    quarter_final_prob REAL,
    round_of_16_prob REAL,
    avg_goals_scored REAL DEFAULT 0.0,
    avg_goals_conceded REAL DEFAULT 0.0,
    model_version TEXT DEFAULT '1.0.0',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
"""


def get_connection() -> sqlite3.Connection:
    """Get a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def upsert_team(conn: sqlite3.Connection, team: dict) -> None:
    """Insert or update a team record. Missing optional keys default to None."""
    defaults = {
        "fifa_rank": 0,
        "elo_rating": 1500.0,
        "confederation": "",
        "market_value": None,
    }
    for key, default in defaults.items():
        team.setdefault(key, default)
    conn.execute(
        """INSERT OR REPLACE INTO teams (id, name, "group", fifa_rank, elo_rating, confederation, market_value)
           VALUES (:id, :name, :group, :fifa_rank, :elo_rating, :confederation, :market_value)""",
        team,
    )


def upsert_match(conn: sqlite3.Connection, match: dict) -> None:
    """Insert or update a match record. Missing optional keys default to None."""
    defaults = {
        "group": None,
        "match_date": None,
        "venue": None,
        "city": None,
        "home_score": None,
        "away_score": None,
        "status": "scheduled",
    }
    for key, default in defaults.items():
        match.setdefault(key, default)
    conn.execute(
        """INSERT OR REPLACE INTO matches (id, home_team_id, away_team_id, stage, "group",
           match_date, venue, city, home_score, away_score, status)
           VALUES (:id, :home_team_id, :away_team_id, :stage, :group,
           :match_date, :venue, :city, :home_score, :away_score, :status)""",
        match,
    )


def save_prediction(conn: sqlite3.Connection, pred: dict) -> None:
    """Save a match prediction."""
    conn.execute(
        """INSERT INTO predictions (match_id, home_team_id, away_team_id,
           home_win_prob, draw_prob, away_win_prob, predicted_home_goals,
           predicted_away_goals, elo_home_win_prob, poisson_home_win_prob,
           lightgbm_home_win_prob, llm_correction, llm_narrative, model_version)
           VALUES (:match_id, :home_team_id, :away_team_id,
           :home_win_prob, :draw_prob, :away_win_prob, :predicted_home_goals,
           :predicted_away_goals, :elo_home_win_prob, :poisson_home_win_prob,
           :lightgbm_home_win_prob, :llm_correction, :llm_narrative, :model_version)""",
        pred,
    )


def save_tournament_prediction(conn: sqlite3.Connection, pred: dict) -> None:
    """Save a tournament-level team prediction."""
    conn.execute(
        """INSERT INTO tournament_predictions (team_id, champion_prob, final_prob,
           semi_final_prob, quarter_final_prob, round_of_16_prob,
           avg_goals_scored, avg_goals_conceded, model_version)
           VALUES (:team_id, :champion_prob, :final_prob,
           :semi_final_prob, :quarter_final_prob, :round_of_16_prob,
           :avg_goals_scored, :avg_goals_conceded, :model_version)""",
        pred,
    )
