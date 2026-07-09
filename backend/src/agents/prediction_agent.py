"""
Prediction Agent — runs all four models and produces match predictions.
"""

import logging
from typing import Any

from ..data.database import get_connection, save_prediction
from ..data.loader import get_teams_map
from ..features.pipeline import FeaturePipeline
from ..models.elo_model import EloModel
from ..models.poisson import PoissonModel
from ..models.lightgbm_model import LightGBMModel
from ..models.llm_analyzer import LLMAnalyzer
from ..models.ensemble import EnsembleModel
from .base import BaseAgent

logger = logging.getLogger(__name__)


class PredictionAgent(BaseAgent):
    """Runs all prediction models and fuses results via ensemble."""

    def __init__(self, pipeline: FeaturePipeline, poisson_model: PoissonModel,
                 lightgbm_model: LightGBMModel, llm_analyzer: LLMAnalyzer):
        super().__init__("PredictionAgent")
        self.pipeline = pipeline
        self.ensemble = EnsembleModel(pipeline, poisson_model, lightgbm_model, llm_analyzer)
        self.elo_model = self.ensemble.elo_model
        self.poisson_model = poisson_model
        self.lightgbm_model = lightgbm_model

    def run(self, context: dict) -> dict:
        """Predict all scheduled matches and store results.

        Expects context to contain:
        - 'teams': {team_id: team_dict}
        - 'scheduled_matches': list of match dicts
        - 'pipeline': FeaturePipeline (fitted)
        """
        self.log("Starting match predictions...")

        teams = context.get("teams", {})
        scheduled = context.get("scheduled_matches", [])
        predictions = []

        conn = get_connection()
        try:
            for match in scheduled:
                hid = match["home_team_id"]
                aid = match["away_team_id"]

                if hid == "TBD" or aid == "TBD":
                    self.log(f"Skipping {match['id']} — teams not yet determined.")
                    continue

                home_name = teams.get(hid, {}).get("name", hid)
                away_name = teams.get(aid, {}).get("name", aid)
                stage = match["stage"]

                self.log(f"Predicting: {home_name} vs {away_name} ({stage})")

                # Run ensemble prediction
                pred = self.ensemble.predict(hid, aid, stage, home_name, away_name)
                pred["match_id"] = match["id"]

                # Save to database
                save_prediction(conn, {
                    "match_id": match["id"],
                    "home_team_id": hid,
                    "away_team_id": aid,
                    "home_win_prob": pred["home_win_prob"],
                    "draw_prob": pred["draw_prob"],
                    "away_win_prob": pred["away_win_prob"],
                    "predicted_home_goals": pred["predicted_home_goals"],
                    "predicted_away_goals": pred["predicted_away_goals"],
                    "elo_home_win_prob": pred["elo_home_win_prob"],
                    "poisson_home_win_prob": pred["poisson_home_win_prob"],
                    "lightgbm_home_win_prob": pred["lightgbm_home_win_prob"],
                    "llm_correction": pred["llm_correction"],
                    "llm_narrative": pred["llm_narrative"],
                    "model_version": "1.0.0",
                })

                predictions.append(pred)

            conn.commit()
        finally:
            conn.close()

        context["predictions"] = predictions
        self.log(f"Completed {len(predictions)} match predictions.")
        return context
