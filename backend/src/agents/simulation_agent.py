"""
Simulation Agent — runs Monte Carlo tournament simulation.
"""

import logging
from typing import Any

from ..data.database import get_connection, save_tournament_prediction
from ..simulation.tournament import TournamentSimulator
from ..simulation.monte_carlo import MonteCarloEngine
from ..config import MC_ITERATIONS, MC_RANDOM_SEED
from .base import BaseAgent

logger = logging.getLogger(__name__)


class SimulationAgent(BaseAgent):
    """Runs Monte Carlo simulations for tournament-level predictions."""

    def __init__(self, simulator: TournamentSimulator, mc_engine: MonteCarloEngine):
        super().__init__("SimulationAgent")
        self.simulator = simulator
        self.mc_engine = mc_engine

    def run(self, context: dict) -> dict:
        """Run Monte Carlo tournament simulation.

        Expects context to contain:
        - 'teams': team map
        - 'predictions': list of match predictions (for remaining matches)
        - 'completed_matches': for actual results
        """
        self.log(f"Running {MC_ITERATIONS} Monte Carlo simulations...")

        teams = context.get("teams", {})
        predictions = context.get("predictions", [])
        completed = context.get("completed_matches", [])

        # Build probability lookup for remaining matches
        match_probs = {}
        for pred in predictions:
            match_probs[pred["match_id"]] = {
                "home_win": pred["home_win_prob"],
                "draw": pred["draw_prob"],
                "away_win": pred["away_win_prob"],
                "home_goals": pred["predicted_home_goals"],
                "away_goals": pred["predicted_away_goals"],
            }

        # Initialize tournament state with completed results
        self.simulator.load_teams(teams)
        self.simulator.load_completed_matches(completed)

        # Run simulations
        results = self.mc_engine.run(
            simulator=self.simulator,
            match_probabilities=match_probs,
            n_iterations=MC_ITERATIONS,
        )

        # Compute tournament predictions
        tournament_preds = []
        for team_id in results["champion_counts"]:
            count = results["champion_counts"].get(team_id, 0)
            final_count = results["final_counts"].get(team_id, 0)
            semi_count = results["semi_final_counts"].get(team_id, 0)
            qf_count = results["quarter_final_counts"].get(team_id, 0)
            r16_count = results["round_of_16_counts"].get(team_id, 0)

            team_name = teams.get(team_id, {}).get("name", team_id)
            n = results["total_iterations"]
            from ..data.constants import ALIVE_TEAMS

            pred = {
                "team_id": team_id,
                "team_name": team_name,
                "champion_prob": min(count / n, 1.0),
                "final_prob": min(final_count / n, 1.0),
                "semi_final_prob": min(semi_count / n, 1.0),
                "quarter_final_prob": 1.0 if team_id in ALIVE_TEAMS else min(qf_count / n, 1.0),
                "round_of_16_prob": min(r16_count / n, 1.0),
                "avg_goals_scored": results["team_goals_scored"].get(team_id, 0) / max(count, 1),
                "avg_goals_conceded": results["team_goals_conceded"].get(team_id, 0) / max(count, 1),
                "model_version": "1.0.0",
            }
            tournament_preds.append(pred)

        # Sort by champion probability
        tournament_preds.sort(key=lambda x: x["champion_prob"], reverse=True)

        # Save to database
        conn = get_connection()
        try:
            for tp in tournament_preds:
                save_tournament_prediction(conn, {
                    "team_id": tp["team_id"],
                    "champion_prob": tp["champion_prob"],
                    "final_prob": tp["final_prob"],
                    "semi_final_prob": tp["semi_final_prob"],
                    "quarter_final_prob": tp["quarter_final_prob"],
                    "round_of_16_prob": tp["round_of_16_prob"],
                    "avg_goals_scored": tp["avg_goals_scored"],
                    "avg_goals_conceded": tp["avg_goals_conceded"],
                    "model_version": "1.0.0",
                })
            conn.commit()
        finally:
            conn.close()

        context["tournament_predictions"] = tournament_preds
        context["simulation_stats"] = {
            "total_iterations": n,
            "teams_with_champion_prob_above_1pct": sum(
                1 for tp in tournament_preds if tp["champion_prob"] > 0.01
            ),
        }

        # Top 5 summary
        for i, tp in enumerate(tournament_preds[:5]):
            self.log(
                f"  #{i+1} {tp['team_name']}: "
                f"Champion {tp['champion_prob']:.1%}, "
                f"Final {tp['final_prob']:.1%}, "
                f"SF {tp['semi_final_prob']:.1%}"
            )

        return context
