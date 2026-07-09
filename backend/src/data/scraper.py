"""
Web scraper for 2026 World Cup data.
Falls back to constants.py data when scraping fails.

Currently (July 2026): primarily relies on hardcoded data since the
tournament is in progress and real-time data has been captured.
"""

import json
import logging
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from ..config import DATA_RAW

logger = logging.getLogger(__name__)


class WorldCupScraper:
    """Scraper for FIFA rankings, Elo ratings, and match results."""

    def __init__(self):
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )

    def close(self):
        self.client.close()

    def scrape_fifa_rankings(self) -> list[dict]:
        """Scrape current FIFA world rankings. Falls back to cached data."""
        try:
            # Try to fetch from FIFA official rankings page
            url = "https://inside.fifa.com/en/fifa-rankings"
            resp = self.client.get(url, follow_redirects=True)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                # Parse ranking table — structure varies, attempt extraction
                rankings = self._parse_fifa_table(soup)
                if rankings:
                    self._save_raw("fifa_rankings.json", rankings)
                    return rankings
        except Exception as e:
            logger.warning(f"FIFA ranking scrape failed: {e}")

        # Fall back to cached data
        return self._load_cached("fifa_rankings.json")

    def scrape_elo_ratings(self) -> list[dict]:
        """Scrape Elo ratings from eloratings.net. Falls back to cached data."""
        try:
            url = "https://www.eloratings.net/"
            resp = self.client.get(url, follow_redirects=True)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                ratings = self._parse_elo_table(soup)
                if ratings:
                    self._save_raw("elo_ratings.json", ratings)
                    return ratings
        except Exception as e:
            logger.warning(f"Elo rating scrape failed: {e}")

        return self._load_cached("elo_ratings.json")

    def scrape_match_results(self) -> list[dict]:
        """Scrape 2026 World Cup match results. Falls back to cached data."""
        try:
            url = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums"
            resp = self.client.get(url, follow_redirects=True)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                results = self._parse_match_results(soup)
                if results:
                    self._save_raw("match_results.json", results)
                    return results
        except Exception as e:
            logger.warning(f"Match results scrape failed: {e}")

        return self._load_cached("match_results.json")

    def _parse_fifa_table(self, soup: BeautifulSoup) -> list[dict]:
        """Parse FIFA ranking table from HTML."""
        rankings = []
        # Try multiple possible table structures
        table = soup.find("table", class_=lambda c: c and "ranking" in c.lower() if c else False)
        if not table:
            table = soup.find("table")
        if not table:
            return rankings

        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                try:
                    rank = int(cells[0].get_text(strip=True))
                    name = cells[1].get_text(strip=True)
                    rankings.append({"rank": rank, "name": name})
                except (ValueError, IndexError):
                    continue
        return rankings

    def _parse_elo_table(self, soup: BeautifulSoup) -> list[dict]:
        """Parse Elo ratings table from HTML."""
        ratings = []
        table = soup.find("table")
        if not table:
            return ratings

        rows = table.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                try:
                    rank = int(cells[0].get_text(strip=True))
                    name = cells[1].get_text(strip=True)
                    rating = float(cells[2].get_text(strip=True))
                    ratings.append({"rank": rank, "name": name, "rating": rating})
                except (ValueError, IndexError):
                    continue
        return ratings

    def _parse_match_results(self, soup: BeautifulSoup) -> list[dict]:
        """Parse match results from HTML."""
        results = []
        match_cards = soup.find_all("div", class_=lambda c: c and "match" in c.lower() if c else False)
        for card in match_cards:
            # Try to extract teams and scores
            home = card.find(class_=lambda c: c and "home" in c.lower() if c else False)
            away = card.find(class_=lambda c: c and "away" in c.lower() if c else False)
            score = card.find(class_=lambda c: c and "score" in c.lower() if c else False)
            if home and away and score:
                results.append({
                    "home": home.get_text(strip=True),
                    "away": away.get_text(strip=True),
                    "score": score.get_text(strip=True),
                })
        return results

    def _save_raw(self, filename: str, data) -> None:
        """Save scraped data to raw data directory."""
        DATA_RAW.mkdir(parents=True, exist_ok=True)
        path = DATA_RAW / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved raw data to {path}")

    def _load_cached(self, filename: str) -> list:
        """Load cached data from raw data directory."""
        path = DATA_RAW / filename
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


# Convenience function
def scrape_all() -> dict:
    """Run all scrapers and return combined results."""
    scraper = WorldCupScraper()
    try:
        rankings = scraper.scrape_fifa_rankings()
        elo = scraper.scrape_elo_ratings()
        results = scraper.scrape_match_results()
        return {
            "fifa_rankings": len(rankings),
            "elo_ratings": len(elo),
            "match_results": len(results),
        }
    finally:
        scraper.close()
