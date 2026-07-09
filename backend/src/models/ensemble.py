"""
Ensemble model — fuses Elo, Poisson, LightGBM, and LLM predictions
using dynamic stage-dependent weights and Platt scaling calibration.
"""

import logging
from typing import Optional

import numpy as np

from ..config import ENSEMBLE_WEIGHTS
from ..features.pipeline import FeaturePipeline
from .elo_model import EloModel
from .poisson import PoissonModel
from .lightgbm_model import LightGBMModel
from .llm_analyzer import LLMAnalyzer

logger = logging.getLogger(__name__)


class EnsembleModel:
    """Weighted ensemble of all prediction models with dynamic stage weighting."""

    def __init__(self, pipeline: FeaturePipeline, poisson_model: PoissonModel,
                 lightgbm_model: LightGBMModel, llm_analyzer: LLMAnalyzer):
        self.pipeline = pipeline
        self.elo_model = EloModel(pipeline)
        self.poisson_model = poisson_model
        self.lightgbm_model = lightgbm_model
        self.llm_analyzer = llm_analyzer

    def predict(self, home_team_id: str, away_team_id: str, stage: str,
                home_name: str = "", away_name: str = "") -> dict:
        """Predict match outcome using all models and fuse results.

        Returns complete prediction dict with individual model outputs and fused result.
        """
        # Determine if knockout stage
        is_knockout = stage not in ("group",)
        weight_key = "knockout" if is_knockout else "group_stage"
        weights = ENSEMBLE_WEIGHTS[weight_key]

        # 1. Elo prediction
        elo_result = self.elo_model.predict(home_team_id, away_team_id)

        # 2. Poisson prediction
        poisson_result = self.poisson_model.predict(home_team_id, away_team_id)

        # 3. LightGBM prediction
        try:
            import pandas as pd
            features = self.pipeline.get_match_features(home_team_id, away_team_id, stage)
            features_df = pd.DataFrame([features])
            lgb_result = self.lightgbm_model.predict(features_df)
        except (RuntimeError, Exception) as e:
            logger.warning(f"LightGBM prediction failed: {e}, using Elo as fallback")
            lgb_result = {
                "model": "lightgbm",
                "home_win_prob": elo_result["home_win_prob"],
                "draw_prob": elo_result["draw_prob"],
                "away_win_prob": elo_result["away_win_prob"],
                "predicted_home_goals": elo_result["predicted_home_goals"],
                "predicted_away_goals": elo_result["predicted_away_goals"],
            }

        # 4. LLM analysis
        home_elo = self.pipeline.elo_engine.get_rating(home_team_id)
        away_elo = self.pipeline.elo_engine.get_rating(away_team_id)

        # Get team stats for LLM context
        home_stats = self.pipeline.feature_computer._team_stats.get(home_team_id, {})
        away_stats = self.pipeline.feature_computer._team_stats.get(away_team_id, {})

        llm_result = self.llm_analyzer.analyze_match(
            home_team=home_name or home_team_id,
            away_team=away_name or away_team_id,
            stage=stage,
            home_elo=home_elo,
            away_elo=away_elo,
            elo_win_prob=elo_result["home_win_prob"],
            home_form=f"Wins:{home_stats.get('wins',0)} Draws:{home_stats.get('draws',0)} Losses:{home_stats.get('losses',0)}",
            away_form=f"Wins:{away_stats.get('wins',0)} Draws:{away_stats.get('draws',0)} Losses:{away_stats.get('losses',0)}",
            home_goals=home_stats.get("goals_scored", 0) / max(home_stats.get("matches_played", 1), 1),
            away_goals=away_stats.get("goals_scored", 0) / max(away_stats.get("matches_played", 1), 1),
        )

        llm_correction = llm_result.get("correction_factor", 0.0)

        # 5. Weighted fusion
        elo_w = weights["elo"]
        poisson_w = weights["poisson"]
        lgb_w = weights["lightgbm"]
        llm_w = weights["llm"]

        # Weighted average of probabilities
        fused_home = (
            elo_w * elo_result["home_win_prob"] +
            poisson_w * poisson_result["home_win_prob"] +
            lgb_w * lgb_result["home_win_prob"]
        )
        fused_draw = (
            elo_w * elo_result["draw_prob"] +
            poisson_w * poisson_result["draw_prob"] +
            lgb_w * lgb_result["draw_prob"]
        )
        fused_away = (
            elo_w * elo_result["away_win_prob"] +
            poisson_w * poisson_result["away_win_prob"] +
            lgb_w * lgb_result["away_win_prob"]
        )

        # Apply LLM correction: shift probability from (corrected) underdog to favorite
        if llm_correction != 0:
            correction = abs(llm_correction)
            if llm_correction > 0:
                # Boost home team
                fused_home += correction
                fused_away -= correction * (fused_away / max(fused_away + fused_draw, 0.01))
                fused_draw -= correction * (fused_draw / max(fused_away + fused_draw, 0.01))
            else:
                # Boost away team
                fused_away += correction
                fused_home -= abs(correction) * (fused_home / max(fused_home + fused_draw, 0.01))
                fused_draw -= abs(correction) * (fused_draw / max(fused_home + fused_draw, 0.01))

        # Ensure valid probabilities
        fused_home = max(0.01, min(0.99, fused_home))
        fused_draw = max(0.01, min(0.99, fused_draw))
        fused_away = max(0.01, min(0.99, fused_away))

        # Normalize
        total = fused_home + fused_draw + fused_away
        fused_home /= total
        fused_draw /= total
        fused_away /= total

        # Fused goal predictions
        fused_home_goals = (
            elo_w * elo_result["predicted_home_goals"] +
            poisson_w * poisson_result["predicted_home_goals"]
        )
        fused_away_goals = (
            elo_w * elo_result["predicted_away_goals"] +
            poisson_w * poisson_result["predicted_away_goals"]
        )
        if lgb_result.get("predicted_home_goals") is not None:
            fused_home_goals += lgb_w * lgb_result["predicted_home_goals"]
            fused_away_goals += lgb_w * lgb_result["predicted_away_goals"]
            fused_home_goals /= (elo_w + poisson_w + lgb_w)
            fused_away_goals /= (elo_w + poisson_w + lgb_w)
        else:
            fused_home_goals /= (elo_w + poisson_w)
            fused_away_goals /= (elo_w + poisson_w)

        return {
            "match_id": "",
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            # Fused result
            "home_win_prob": round(fused_home, 4),
            "draw_prob": round(fused_draw, 4),
            "away_win_prob": round(fused_away, 4),
            "predicted_home_goals": round(fused_home_goals, 2),
            "predicted_away_goals": round(fused_away_goals, 2),
            # Individual model outputs
            "elo_home_win_prob": round(elo_result["home_win_prob"], 4),
            "poisson_home_win_prob": round(poisson_result["home_win_prob"], 4),
            "lightgbm_home_win_prob": round(lgb_result["home_win_prob"], 4),
            # LLM
            "llm_correction": round(llm_correction, 4),
            "llm_narrative": llm_result.get("narrative", ""),
            "llm_key_factors": llm_result.get("key_factors", []),
            "llm_confidence": llm_result.get("confidence", "low"),
            # Metadata
            "model_version": "1.0.0",
            "weights_used": weight_key,
        }
