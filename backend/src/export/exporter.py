"""
Export predictions to JSON for the React frontend.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..config import FRONTEND_DATA_DIR
from ..data.models import PredictionExport, Team, Match, MatchPrediction, TeamTournamentPrediction

logger = logging.getLogger(__name__)


class Exporter:
    """Exports prediction results to a static JSON file for the frontend."""

    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or FRONTEND_DATA_DIR

    def export(self, context: dict) -> str:
        """Export all predictions to predictions.json.

        Returns the path of the exported file.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Build export data
        teams = context.get("teams", {})
        predictions = context.get("predictions", [])
        tournament_preds = context.get("tournament_predictions", [])
        completed = context.get("completed_matches", [])
        scheduled = context.get("scheduled_matches", [])

        export = {
            "generated_at": datetime.now().isoformat(),
            "model_version": "1.0.0",
            "monte_carlo_iterations": context.get("simulation_stats", {}).get("total_iterations", 5000),
            "teams": [self._team_to_dict(t) for t in teams.values() if t.get("id") != "TBD"],
            "matches": ([self._match_to_dict(m) for m in completed] +
                       [self._match_to_dict(m) for m in scheduled]),
            "match_predictions": [self._pred_to_dict(p) for p in predictions],
            "tournament_predictions": [self._tp_to_dict(tp) for tp in tournament_preds],
            "llm_narrative": context.get("llm_narrative", ""),
        }

        output_path = self.output_dir / "predictions.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)

        logger.info(f"Exported predictions to {output_path} "
                     f"({len(export['teams'])} teams, {len(predictions)} predictions)")

        # Also export to data directory
        data_export = Path("data/predictions/predictions.json")
        data_export.parent.mkdir(parents=True, exist_ok=True)
        with open(data_export, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)

        return str(output_path)

    def _team_to_dict(self, team: dict) -> dict:
        return {
            "id": team.get("id"),
            "name": team.get("name"),
            "group": team.get("group"),
            "fifa_rank": team.get("fifa_rank", 0),
            "elo_rating": team.get("elo_rating", 1500),
            "confederation": team.get("confederation", ""),
        }

    def _match_to_dict(self, match: dict) -> dict:
        return {
            "id": match.get("id"),
            "home_team_id": match.get("home_team_id"),
            "away_team_id": match.get("away_team_id"),
            "stage": match.get("stage"),
            "group": match.get("group"),
            "match_date": match.get("match_date"),
            "venue": match.get("venue"),
            "city": match.get("city"),
            "home_score": match.get("home_score"),
            "away_score": match.get("away_score"),
            "status": match.get("status"),
        }

    def _pred_to_dict(self, pred: dict) -> dict:
        return {
            "match_id": pred.get("match_id"),
            "home_team_id": pred.get("home_team_id"),
            "away_team_id": pred.get("away_team_id"),
            "home_win_prob": pred.get("home_win_prob"),
            "draw_prob": pred.get("draw_prob"),
            "away_win_prob": pred.get("away_win_prob"),
            "predicted_home_goals": pred.get("predicted_home_goals"),
            "predicted_away_goals": pred.get("predicted_away_goals"),
            "elo_home_win_prob": pred.get("elo_home_win_prob"),
            "poisson_home_win_prob": pred.get("poisson_home_win_prob"),
            "lightgbm_home_win_prob": pred.get("lightgbm_home_win_prob"),
            "llm_correction": pred.get("llm_correction", 0),
            "llm_narrative": pred.get("llm_narrative", ""),
            "model_version": pred.get("model_version", "1.0.0"),
        }

    def _tp_to_dict(self, tp: dict) -> dict:
        return {
            "team_id": tp.get("team_id"),
            "team_name": tp.get("team_name"),
            "champion_prob": tp.get("champion_prob"),
            "final_prob": tp.get("final_prob"),
            "semi_final_prob": tp.get("semi_final_prob"),
            "quarter_final_prob": tp.get("quarter_final_prob"),
            "round_of_16_prob": tp.get("round_of_16_prob"),
            "avg_goals_scored": tp.get("avg_goals_scored", 0),
            "avg_goals_conceded": tp.get("avg_goals_conceded", 0),
        }
