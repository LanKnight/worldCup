"""
Monte Carlo engine for tournament simulation.
Runs multiple tournament simulations in parallel and aggregates results.
"""

import logging
import random
from collections import defaultdict
from typing import Any

from ..config import MC_ITERATIONS, MC_RANDOM_SEED
from .tournament import TournamentSimulator, TournamentState

logger = logging.getLogger(__name__)


class MonteCarloEngine:
    """Runs Monte Carlo simulations for tournament prediction."""

    def __init__(self, seed: int = MC_RANDOM_SEED):
        self.seed = seed
        random.seed(seed)

    def run(self, simulator: TournamentSimulator, match_probabilities: dict,
            n_iterations: int = MC_ITERATIONS) -> dict:
        """Run Monte Carlo tournament simulations.

        Returns aggregated statistics:
        - champion_counts: {team_id: count}
        - final_counts: {team_id: count}
        - semi_final_counts: {team_id: count}
        - quarter_final_counts: {team_id: count}
        - round_of_16_counts: {team_id: count}
        - total_iterations: int
        - team_goals_scored: {team_id: total_goals}
        - team_goals_conceded: {team_id: total_goals}
        """
        champion_counts: dict[str, int] = defaultdict(int)
        final_counts: dict[str, int] = defaultdict(int)
        semi_final_counts: dict[str, int] = defaultdict(int)
        quarter_final_counts: dict[str, int] = defaultdict(int)
        round_of_16_counts: dict[str, int] = defaultdict(int)
        team_goals_scored: dict[str, int] = defaultdict(int)
        team_goals_conceded: dict[str, int] = defaultdict(int)

        # Only alive teams can progress further
        from ..data.constants import ALIVE_TEAMS

        for i in range(n_iterations):
            if i % 1000 == 0:
                logger.info(f"  Simulation {i}/{n_iterations}...")

            state = simulator.simulate(match_probabilities)

            # Champion = winner of FINAL_1
            champion = state.knockout_winners.get("FINAL_1")
            if champion:
                champion_counts[champion] += 1

            # Finalists = teams in FINAL_1
            # (simplified — every team in SF winner list made the final)
            sf_winners = []
            for key, winner in state.knockout_winners.items():
                if key.startswith("SF_"):
                    sf_winners.append(winner)
                    semi_final_counts[winner] += 1

            # SF losers made semi-final too
            for key, winner in state.knockout_winners.items():
                if key.startswith("QF_"):
                    quarter_final_counts[winner] += 1
                elif key.startswith("R16_"):
                    round_of_16_counts[winner] += 1

            # Accumulate goals
            for tid, goals in state.team_goals_scored.items():
                team_goals_scored[tid] += goals
            for tid, goals in state.team_goals_conceded.items():
                team_goals_conceded[tid] += goals

        return {
            "champion_counts": dict(champion_counts),
            "final_counts": dict(final_counts),
            "semi_final_counts": dict(semi_final_counts),
            "quarter_final_counts": dict(quarter_final_counts),
            "round_of_16_counts": dict(round_of_16_counts),
            "total_iterations": n_iterations,
            "team_goals_scored": dict(team_goals_scored),
            "team_goals_conceded": dict(team_goals_conceded),
        }
