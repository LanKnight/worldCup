"""
Data loader: populates the SQLite database from constants and scraped data.
"""

import logging
from typing import Optional

from . import constants
from .database import get_connection, init_db, upsert_team, upsert_match

logger = logging.getLogger(__name__)


def load_teams(conn=None) -> int:
    """Load teams from constants into the database. Returns count loaded."""
    should_close = conn is None
    if conn is None:
        init_db()
        conn = get_connection()

    try:
        count = 0
        for team in constants.TEAMS:
            upsert_team(conn, team)
            count += 1
        conn.commit()
        logger.info(f"Loaded {count} teams into database.")
        return count
    finally:
        if should_close:
            conn.close()


def load_matches(conn=None) -> int:
    """Load matches from constants into the database. Returns count loaded."""
    should_close = conn is None
    if conn is None:
        init_db()
        conn = get_connection()

    try:
        count = 0
        for match in constants.MATCHES:
            upsert_match(conn, match)
            count += 1
        conn.commit()
        logger.info(f"Loaded {count} matches into database.")
        return count
    finally:
        if should_close:
            conn.close()


def load_all(conn=None) -> dict:
    """Load all seed data (teams + matches) into the database."""
    if conn is None:
        init_db()
        conn = get_connection()
        should_close = True
    else:
        should_close = False

    try:
        n_teams = load_teams(conn)
        n_matches = load_matches(conn)
        return {"teams": n_teams, "matches": n_matches}
    finally:
        if should_close:
            conn.close()


def get_teams_map(conn=None) -> dict:
    """Return a dict mapping team_id -> team dict for quick lookup."""
    should_close = conn is None
    if conn is None:
        conn = get_connection()

    try:
        rows = conn.execute("SELECT * FROM teams").fetchall()
        return {row["id"]: dict(row) for row in rows}
    finally:
        if should_close:
            conn.close()


def get_completed_matches(conn=None) -> list:
    """Return all completed matches sorted by date."""
    should_close = conn is None
    if conn is None:
        conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM matches WHERE status = 'completed' ORDER BY match_date"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if should_close:
            conn.close()


def get_scheduled_matches(conn=None) -> list:
    """Return all scheduled (not yet played) matches sorted by date."""
    should_close = conn is None
    if conn is None:
        conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM matches WHERE status = 'scheduled' ORDER BY match_date"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if should_close:
            conn.close()


def get_matches_by_stage(conn=None, stage: str = "group") -> list:
    """Return all matches for a given tournament stage."""
    should_close = conn is None
    if conn is None:
        conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM matches WHERE stage = ? ORDER BY match_date", (stage,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if should_close:
            conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = load_all()
    print(f"Database loaded: {result}")
