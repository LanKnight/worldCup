"""
Data Agent — responsible for data collection, validation, and loading.
"""

from ..data.database import get_connection, init_db
from ..data.loader import load_all, get_teams_map, get_completed_matches, get_scheduled_matches
from ..data.scraper import scrape_all
from .base import BaseAgent


class DataAgent(BaseAgent):
    """Collects, validates, and loads World Cup data."""

    def __init__(self):
        super().__init__("DataAgent")

    def run(self, context: dict) -> dict:
        """Collect data from constants and optional web scraping.

        Modifies context in-place and returns it.
        """
        self.log("Initializing database...")
        init_db()

        # Load seed data from constants
        self.log("Loading seed data from constants...")
        result = load_all()
        self.log(f"Loaded {result['teams']} teams and {result['matches']} matches from constants.")

        # Attempt web scraping for additional data
        try:
            self.log("Attempting web scraping for latest data...")
            scraped = scrape_all()
            self.log(f"Scraped: {scraped}")
        except Exception as e:
            self.warn(f"Web scraping skipped: {e}")

        # Load data into context
        conn = get_connection()
        try:
            context["teams"] = get_teams_map(conn)
            context["completed_matches"] = get_completed_matches(conn)
            context["scheduled_matches"] = get_scheduled_matches(conn)
        finally:
            conn.close()

        n_completed = len(context["completed_matches"])
        n_scheduled = len(context["scheduled_matches"])
        self.log(f"Data ready: {n_completed} completed matches, {n_scheduled} matches to predict.")

        context["data_agent"] = {"status": "ok", "teams_loaded": result["teams"]}
        return context
