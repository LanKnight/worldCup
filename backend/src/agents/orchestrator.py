"""
Main Orchestrator Agent — coordinates the full prediction pipeline.
"""

import logging
import time
from typing import Any

from ..data.database import init_db, get_connection
from ..data.loader import load_all
from ..features.pipeline import FeaturePipeline
from ..models.poisson import PoissonModel
from ..models.lightgbm_model import LightGBMModel
from ..models.llm_analyzer import LLMAnalyzer
from ..simulation.tournament import TournamentSimulator
from ..simulation.monte_carlo import MonteCarloEngine
from ..export.exporter import Exporter
from .data_agent import DataAgent
from .prediction_agent import PredictionAgent
from .llm_agent import LLMAgent
from .simulation_agent import SimulationAgent

logger = logging.getLogger(__name__)


class Orchestrator:
    """Master orchestrator that coordinates all agents in the prediction pipeline."""

    def __init__(self):
        self.data_agent = DataAgent()
        self.pipeline = FeaturePipeline()
        self.poisson_model = PoissonModel()
        self.lightgbm_model = LightGBMModel()
        self.llm_analyzer = LLMAnalyzer()
        self.llm_agent = LLMAgent(self.llm_analyzer)
        self.simulator = TournamentSimulator()
        self.mc_engine = MonteCarloEngine()
        self.exporter = Exporter()

        # Agents that depend on models (created after models are initialized)
        self.prediction_agent = None
        self.simulation_agent = None

    def run(self) -> dict:
        """Execute the full prediction pipeline.

        Steps:
        1. DataAgent: collect and load all data
        2. FeaturePipeline: compute Elo, tournament stats, features
        3. Poisson + LightGBM: train models
        4. PredictionAgent: predict all scheduled matches
        5. SimulationAgent: Monte Carlo tournament simulation
        6. LLMAgent: generate champion analysis narrative
        7. Exporter: export predictions to JSON for frontend
        """
        context: dict[str, Any] = {}
        start_time = time.time()

        logger.info("=" * 60)
        logger.info("2026 WORLD CUP PREDICTION PIPELINE STARTING")
        logger.info("=" * 60)

        # Step 1: Data Collection
        logger.info("\n[Step 1/7] Data Collection...")
        context = self.data_agent.run(context)

        # Step 2: Feature Engineering
        logger.info("\n[Step 2/7] Feature Pipeline...")
        self.pipeline.run()
        context["pipeline"] = self.pipeline

        # Step 3: Train Models
        logger.info("\n[Step 3/7] Training Models...")

        # Fit Poisson on tournament data
        completed = context.get("completed_matches", [])
        teams = context.get("teams", {})
        logger.info(f"  Fitting Poisson model on {len(completed)} completed matches...")
        self.poisson_model.fit(completed, teams)

        # Train LightGBM on historical data
        logger.info("  Training LightGBM on historical data...")
        self._train_lightgbm()

        # Step 4: Match Predictions
        logger.info("\n[Step 4/7] Match Predictions...")
        self.prediction_agent = PredictionAgent(
            self.pipeline, self.poisson_model, self.lightgbm_model, self.llm_analyzer
        )
        context = self.prediction_agent.run(context)

        # Step 5: Tournament Simulation
        logger.info("\n[Step 5/7] Tournament Simulation...")
        self.simulation_agent = SimulationAgent(self.simulator, self.mc_engine)
        context = self.simulation_agent.run(context)

        # Step 6: LLM Narrative
        logger.info("\n[Step 6/7] LLM Champion Analysis...")
        context = self.llm_agent.run(context)

        # Step 7: Export
        logger.info("\n[Step 7/7] Exporting Results...")
        self.exporter.export(context)

        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"PIPELINE COMPLETE in {elapsed:.1f}s")
        logger.info("=" * 60)

        # Print summary
        self._print_summary(context)

        return context

    def _train_lightgbm(self) -> None:
        """Train LightGBM on historical World Cup data + 2026 tournament data."""
        import pandas as pd

        from ..data.historical import HISTORICAL_MATCHES
        from ..data.loader import get_completed_matches

        # Combine historical + 2026 completed data for training
        all_matches = list(HISTORICAL_MATCHES)

        # Add 2026 completed matches with feature computation
        completed_2026 = get_completed_matches()

        # For historical matches, we need to build Elo differently
        # Use a separate Elo instance for historical context
        historical_elo = FeaturePipeline()
        historical_elo.elo_engine.load_ratings(
            [{"id": tid, "elo_rating": 1500} for tid in self._all_team_ids()]
        )

        # Train on combined dataset
        try:
            # For now, use completed 2026 data which has rich features
            df_2026 = self.pipeline.get_features_dataframe(completed_2026)

            if len(df_2026) >= 10:
                self.lightgbm_model.train(df_2026)
                logger.info(f"  LightGBM trained on {len(df_2026)} 2026 tournament matches.")
            else:
                logger.warning("  Insufficient training data for LightGBM. Using Elo/Poisson baseline only.")
        except Exception as e:
            logger.warning(f"  LightGBM training failed: {e}. Using Elo/Poisson baseline only.")

    def _all_team_ids(self) -> set[str]:
        """Get all unique team IDs from historical data and 2026 data."""
        from ..data.constants import TEAMS
        return {t["id"] for t in TEAMS if t["id"] != "TBD"}

    def _print_summary(self, context: dict) -> None:
        """Print a human-readable summary of results."""
        tournament_preds = context.get("tournament_predictions", [])
        predictions = context.get("predictions", [])
        teams = context.get("teams", {})

        print("\n" + "=" * 60)
        print("2026 WORLD CUP CHAMPION PREDICTION")
        print("=" * 60)

        if tournament_preds:
            print("\nTop 5 Championship Contenders:")
            for i, tp in enumerate(tournament_preds[:5]):
                bar = "█" * int(tp["champion_prob"] * 50)
                print(f"  {i+1}. {tp['team_name']:<20} {tp['champion_prob']:>6.1%} {bar}")

        if predictions:
            print("\nQuarterfinal Predictions:")
            for pred in predictions:
                home = teams.get(pred["home_team_id"], {}).get("name", pred["home_team_id"])
                away = teams.get(pred["away_team_id"], {}).get("name", pred["away_team_id"])
                print(f"  {home} vs {away}")
                print(f"    Home: {pred['home_win_prob']:.1%} | Draw: {pred['draw_prob']:.1%} | Away: {pred['away_win_prob']:.1%}")
                print(f"    Expected: {pred['predicted_home_goals']} - {pred['predicted_away_goals']}")
                if pred.get("llm_narrative"):
                    print(f"    LLM: {pred['llm_narrative'][:100]}...")
                print()

        if context.get("llm_narrative"):
            print("[LLM Champion Analysis]")
            print(f"  {context['llm_narrative'][:500]}")
            print()

        print(f"Model Version: 1.0.0 | Powered by DeepSeek API")
