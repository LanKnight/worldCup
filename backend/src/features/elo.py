"""
Elo rating system for World Cup teams.
Based on standard Elo with World Cup K-factor and dynamic updates.
"""

import math
from typing import Optional

from ..config import ELO_K_FACTOR, ELO_INITIAL, ELO_HOME_ADVANTAGE


class EloEngine:
    """Manages Elo ratings for all teams, with match-based updates."""

    def __init__(self, k_factor: float = ELO_K_FACTOR, home_advantage: float = ELO_HOME_ADVANTAGE):
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        self.ratings: dict[str, float] = {}  # team_id -> current Elo

    def load_ratings(self, teams: list[dict]) -> None:
        """Load initial Elo ratings from team data."""
        for team in teams:
            self.ratings[team["id"]] = team.get("elo_rating", ELO_INITIAL)

    def get_rating(self, team_id: str) -> float:
        """Get current Elo rating for a team."""
        return self.ratings.get(team_id, ELO_INITIAL)

    def expected_score(self, rating_a: float, rating_b: float, neutral: bool = True) -> float:
        """Calculate expected score for team A against team B.
        Uses standard Elo formula: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
        Home advantage adds to the home team's rating if neutral=False.
        """
        if not neutral:
            rating_a += self.home_advantage
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))

    def win_probability(self, team_a: str, team_b: str, neutral: bool = True) -> float:
        """Calculate win probability for team_a vs team_b (including draw).
        Returns: (home_win_prob, draw_prob, away_win_prob)
        Based on Elo difference.
        """
        ra = self.get_rating(team_a)
        rb = self.get_rating(team_b)

        # Expected score for team A (ignoring home advantage for simplicity here)
        ea = self.expected_score(ra, rb, neutral=neutral)

        # Convert expected score to win/draw/loss probabilities
        # Using empirical relationship derived from historical World Cup data
        # Draw probability peaks when teams are evenly matched
        elo_diff = ra - rb
        if not neutral:
            elo_diff += self.home_advantage

        # Draw probability approximation (Gaussian around 0 Elo diff)
        draw_p = 0.28 * math.exp(-(elo_diff ** 2) / (2 * 300 ** 2))

        # Distribute remaining probability between win and loss
        remaining = 1.0 - draw_p
        home_win = ea * remaining
        away_win = (1.0 - ea) * remaining

        return home_win, draw_p, away_win

    def update_ratings(self, team_a: str, team_b: str, goals_a: int, goals_b: int,
                       neutral: bool = True, k_override: Optional[float] = None) -> tuple[float, float]:
        """Update Elo ratings based on match result. Returns (delta_a, delta_b).

        Uses margin-of-victory multiplier and the actual result (win=1, draw=0.5, loss=0).
        """
        ra = self.get_rating(team_a)
        rb = self.get_rating(team_b)

        # Determine actual result
        if goals_a > goals_b:
            score_a, score_b = 1.0, 0.0
        elif goals_a < goals_b:
            score_a, score_b = 0.0, 1.0
        else:
            score_a, score_b = 0.5, 0.5

        # Expected scores
        ea = self.expected_score(ra, rb, neutral=neutral)
        eb = 1.0 - ea

        # Margin of victory multiplier (capped)
        goal_diff = abs(goals_a - goals_b)
        if goal_diff <= 1:
            margin_mult = 1.0
        elif goal_diff == 2:
            margin_mult = 1.5
        else:
            margin_mult = (11 + goal_diff) / 8  # Formula from FiveThirtyEight

        # Update factor
        k = k_override if k_override is not None else self.k_factor
        k_a = k * margin_mult
        k_b = k * margin_mult

        # Rating changes
        delta_a = k_a * (score_a - ea)
        delta_b = k_b * (score_b - eb)

        # Apply updates
        self.ratings[team_a] = ra + delta_a
        self.ratings[team_b] = rb + delta_b

        return delta_a, delta_b

    def compute_all_ratings(self, matches: list[dict], team_ids: set[str]) -> dict[str, list[float]]:
        """Process all matches chronologically and return rating history per team.
        Returns: {team_id: [rating_before_each_match]}
        """
        # Initialize history
        history: dict[str, list[float]] = {tid: [self.get_rating(tid)] for tid in team_ids}

        for match in sorted(matches, key=lambda m: m.get("match_date", "")):
            if match["status"] != "completed":
                continue
            if match["home_score"] is None or match["away_score"] is None:
                continue

            hid = match["home_team_id"]
            aid = match["away_team_id"]

            # Record pre-match ratings
            for tid in [hid, aid]:
                if tid in history:
                    history[tid].append(self.get_rating(tid))

            # Update ratings
            neutral = match.get("stage", "group") != "group" or hid not in ["USA", "MEX", "CAN"]
            self.update_ratings(hid, aid, match["home_score"], match["away_score"], neutral=neutral)

        return history

    def get_top_n(self, n: int = 10) -> list[tuple[str, float]]:
        """Get top N teams by current Elo rating."""
        sorted_teams = sorted(self.ratings.items(), key=lambda x: x[1], reverse=True)
        return sorted_teams[:n]

    def get_elo_diff(self, team_a: str, team_b: str) -> float:
        """Get Elo rating difference (team_a - team_b)."""
        return self.get_rating(team_a) - self.get_rating(team_b)
