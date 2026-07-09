"""
Elo-based match prediction model.
Wraps the Elo engine for standalone prediction.
"""

import logging
from typing import Optional

from ..features.elo import EloEngine
from ..features.pipeline import FeaturePipeline

logger = logging.getLogger(__name__)


class EloModel:
    """Elo-based predictor for match outcomes."""

    def __init__(self, pipeline: FeaturePipeline):
        self.pipeline = pipeline

    def predict(self, home_team_id: str, away_team_id: str,
                neutral: bool = True) -> dict:
        """Predict match outcome using Elo ratings.
        Returns dict with win/draw/loss probabilities and expected goals.
        """
        home_win, draw, away_win = self.pipeline.get_elo_win_prob(
            home_team_id, away_team_id, neutral=neutral
        )

        # Estimate expected goals from Elo difference
        elo_diff = self.pipeline.elo_engine.get_elo_diff(home_team_id, away_team_id)
        # Base: ~1.4 goals per team, adjust by Elo difference
        base_goals = 1.4
        goal_factor = 1.0 + (elo_diff / 400) * 0.5  # ±0.5 goal swing per 400 Elo points
        home_goals = base_goals * goal_factor
        away_goals = base_goals * (2.0 - goal_factor)

        # Clamp
        home_goals = max(0.3, min(4.0, home_goals))
        away_goals = max(0.3, min(4.0, away_goals))

        return {
            "model": "elo",
            "home_win_prob": home_win,
            "draw_prob": draw,
            "away_win_prob": away_win,
            "predicted_home_goals": round(home_goals, 2),
            "predicted_away_goals": round(away_goals, 2),
            "elo_home": self.pipeline.elo_engine.get_rating(home_team_id),
            "elo_away": self.pipeline.elo_engine.get_rating(away_team_id),
            "elo_diff": elo_diff,
        }
