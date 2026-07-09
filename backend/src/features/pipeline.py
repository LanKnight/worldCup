"""
Feature engineering pipeline — orchestrates Elo computation,
tournament stats, and match-level feature assembly.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

from ..data.database import get_connection
from ..data.loader import get_teams_map, get_completed_matches
from .elo import EloEngine
from .base_features import FeatureComputer

logger = logging.getLogger(__name__)


class FeaturePipeline:
    """End-to-end feature engineering pipeline."""

    def __init__(self):
        self.elo_engine = EloEngine()
        self.feature_computer = FeatureComputer(self.elo_engine)
        self._is_fitted = False

    def run(self, conn=None) -> None:
        """Run the full feature pipeline:
        1. Load teams and initialize Elo ratings
        2. Process all completed matches to compute Elo history and tournament stats
        3. Marks pipeline as fitted
        """
        should_close = conn is None
        if conn is None:
            conn = get_connection()

        try:
            # Load teams
            teams = get_teams_map(conn)
            self.elo_engine.load_ratings(list(teams.values()))

            # Exclude TBD from Elo
            if "TBD" in self.elo_engine.ratings:
                del self.elo_engine.ratings["TBD"]

            # Process completed matches to build Elo history and stats
            completed = get_completed_matches(conn)
            team_ids = {t["id"] for t in teams.values() if t["id"] != "TBD"}
            self.elo_engine.compute_all_ratings(completed, team_ids)

            # Compute tournament stats
            self.feature_computer.compute_team_tournament_stats(completed)

            self._is_fitted = True
            logger.info(
                f"FeaturePipeline fitted: {len(self.elo_engine.ratings)} teams, "
                f"{len(completed)} matches processed"
            )
        finally:
            if should_close:
                conn.close()

    def get_match_features(self, home_team_id: str, away_team_id: str,
                           stage: str) -> dict:
        """Get feature vector for a specific match."""
        if not self._is_fitted:
            raise RuntimeError("FeaturePipeline must be run() before get_match_features()")
        return self.feature_computer.compute_match_features(home_team_id, away_team_id, stage)

    def get_elo_win_prob(self, home_team_id: str, away_team_id: str,
                         neutral: bool = True) -> tuple[float, float, float]:
        """Get Elo-based win/draw/loss probabilities."""
        return self.elo_engine.win_probability(home_team_id, away_team_id, neutral=neutral)

    def get_elo_ratings(self) -> dict[str, float]:
        """Get current Elo ratings for all teams."""
        return dict(self.elo_engine.ratings)

    def get_top_teams(self, n: int = 10) -> list[tuple[str, float]]:
        """Get top N teams by Elo rating."""
        return self.elo_engine.get_top_n(n)

    def get_features_dataframe(self, matches: list[dict]) -> pd.DataFrame:
        """Generate feature DataFrame for a list of matches (for LightGBM training/prediction)."""
        if not self._is_fitted:
            raise RuntimeError("FeaturePipeline must be run() before get_features_dataframe()")

        rows = []
        for match in matches:
            if match["home_team_id"] == "TBD" or match["away_team_id"] == "TBD":
                continue
            features = self.get_match_features(
                match["home_team_id"], match["away_team_id"], match["stage"]
            )
            features["match_id"] = match["id"]
            if match["home_score"] is not None:
                # Determine outcome for training
                if match["home_score"] > match["away_score"]:
                    features["outcome"] = 0  # home win
                elif match["home_score"] == match["away_score"]:
                    features["outcome"] = 1  # draw
                else:
                    features["outcome"] = 2  # away win
                features["home_goals"] = match["home_score"]
                features["away_goals"] = match["away_score"]
            rows.append(features)

        return pd.DataFrame(rows)
