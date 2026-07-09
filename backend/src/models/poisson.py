"""
Bivariate Poisson model for match score prediction.
Models each team's goals as Poisson(attack_strength * opponent_defense_weakness).
"""

import logging
from typing import Optional

import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

from ..config import POISSON_MAX_GOALS
from ..data.database import get_connection
from ..data.loader import get_completed_matches, get_teams_map

logger = logging.getLogger(__name__)


class PoissonModel:
    """Bivariate Poisson model for World Cup match prediction."""

    def __init__(self, max_goals: int = POISSON_MAX_GOALS):
        self.max_goals = max_goals
        self.attack: dict[str, float] = {}     # team_id -> attack strength
        self.defense: dict[str, float] = {}     # team_id -> defense weakness
        self.home_advantage: float = 0.3        # home goal bonus
        self._league_avg_goals: float = 1.4

    def fit(self, matches: list[dict], teams: dict[str, dict]) -> None:
        """Fit Poisson model parameters from completed matches using MLE."""
        team_ids = [tid for tid in teams.keys() if tid != "TBD"]

        # Initialize all teams with neutral values
        for tid in team_ids:
            self.attack[tid] = 1.0
            self.defense[tid] = 1.0

        # Build match matrix
        home_teams = []
        away_teams = []
        home_goals = []
        away_goals = []

        for match in matches:
            if match["status"] != "completed":
                continue
            hs = match["home_score"]
            aw = match["away_score"]
            if hs is None or aw is None:
                continue
            if match["home_team_id"] == "TBD" or match["away_team_id"] == "TBD":
                continue
            home_teams.append(match["home_team_id"])
            away_teams.append(match["away_team_id"])
            home_goals.append(hs)
            away_goals.append(aw)

        if len(home_goals) < 10:
            logger.warning("Too few matches to fit Poisson model; using defaults.")
            return

        self._league_avg_goals = np.mean(home_goals + away_goals)

        # Simplified MLE: estimate attack/defense iteratively
        # Based on Dixon-Coles approach (simplified)
        for _ in range(20):  # Max iterations
            # Update attack strengths
            for tid in team_ids:
                home_matches = [(aw, gs) for h, aw, gs in zip(home_teams, away_teams, home_goals) if h == tid]
                away_matches = [(ht, gs) for ht, aw, gs in zip(home_teams, away_teams, away_goals) if aw == tid]

                total_expected = 0.0
                total_actual = 0.0

                for opp_id, gs in home_matches:
                    expected = self.attack.get(tid, 1.0) * self.defense.get(opp_id, 1.0) * (1.0 + self.home_advantage)
                    total_expected += expected
                    total_actual += gs

                for opp_id, gs in away_matches:
                    expected = self.attack.get(tid, 1.0) * self.defense.get(opp_id, 1.0)
                    total_expected += expected
                    total_actual += gs

                if total_expected > 0:
                    self.attack[tid] = total_actual / total_expected

            # Update defense strengths
            for tid in team_ids:
                home_matches = [(aw, gs) for h, aw, gs in zip(home_teams, away_teams, home_goals) if aw == tid]
                away_matches = [(ht, gs) for ht, aw, gs in zip(home_teams, away_teams, away_goals) if ht == tid]

                total_expected = 0.0
                total_actual = 0.0

                for opp_id, gs in home_matches:
                    expected = self.attack.get(opp_id, 1.0) * self.defense.get(tid, 1.0) * (1.0 + self.home_advantage)
                    total_expected += expected
                    total_actual += gs

                for opp_id, gs in away_matches:
                    expected = self.attack.get(opp_id, 1.0) * self.defense.get(tid, 1.0)
                    total_expected += expected
                    total_actual += gs

                if total_expected > 0:
                    self.defense[tid] = total_actual / total_expected

            # Normalize attack to mean 1.0
            mean_attack = np.mean(list(self.attack.values()))
            if mean_attack > 0:
                for tid in self.attack:
                    self.attack[tid] /= mean_attack
                    self.defense[tid] *= mean_attack

        logger.info(f"Poisson model fitted on {len(home_goals)} matches. "
                    f"League avg goals: {self._league_avg_goals:.2f}")

    def _expected_goals(self, home_team: str, away_team: str) -> tuple[float, float]:
        """Compute expected goals for both teams."""
        home_lambda = (self.attack.get(home_team, 1.0) *
                       self.defense.get(away_team, 1.0) *
                       (1.0 + self.home_advantage))
        away_lambda = (self.attack.get(away_team, 1.0) *
                       self.defense.get(home_team, 1.0))
        return max(0.1, home_lambda), max(0.1, away_lambda)

    def predict(self, home_team_id: str, away_team_id: str) -> dict:
        """Predict match outcome using Poisson model.
        Returns win/draw/loss probabilities and expected scoreline.
        """
        home_lambda, away_lambda = self._expected_goals(home_team_id, away_team_id)

        # Compute score probability matrix
        home_win_p = 0.0
        draw_p = 0.0
        away_win_p = 0.0
        best_score = (0, 0)
        best_prob = 0.0

        for i in range(self.max_goals + 1):
            for j in range(self.max_goals + 1):
                prob = poisson.pmf(i, home_lambda) * poisson.pmf(j, away_lambda)
                if prob > best_prob:
                    best_prob = prob
                    best_score = (i, j)
                if i > j:
                    home_win_p += prob
                elif i == j:
                    draw_p += prob
                else:
                    away_win_p += prob

        # Normalize (accounting for truncated distribution)
        total = home_win_p + draw_p + away_win_p
        if total > 0:
            home_win_p /= total
            draw_p /= total
            away_win_p /= total

        return {
            "model": "poisson",
            "home_win_prob": home_win_p,
            "draw_prob": draw_p,
            "away_win_prob": away_win_p,
            "predicted_home_goals": round(home_lambda, 2),
            "predicted_away_goals": round(away_lambda, 2),
            "most_likely_score": f"{best_score[0]}-{best_score[1]}",
            "home_attack": round(self.attack.get(home_team_id, 1.0), 3),
            "away_attack": round(self.attack.get(away_team_id, 1.0), 3),
        }
