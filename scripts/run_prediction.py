#!/usr/bin/env python3
"""
Main entry point for the 2026 World Cup Prediction Pipeline.
Run this script to execute the full prediction workflow:
  1. Data collection
  2. Feature engineering
  3. Model training (Elo, Poisson, LightGBM, DeepSeek LLM)
  4. Match predictions
  5. Monte Carlo tournament simulation
  6. LLM champion analysis
  7. Export results to JSON for frontend

Usage:
    python scripts/run_prediction.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from src.agents.orchestrator import Orchestrator
from src.agents.llm_agent import LLMAgent


def main():
    """Run the full World Cup prediction pipeline."""
    print("""
╔══════════════════════════════════════════════════════════╗
║     2026 FIFA WORLD CUP CHAMPION PREDICTION SYSTEM      ║
║     Multi-Agent AI · Powered by DeepSeek               ║
╚══════════════════════════════════════════════════════════╝
    """)

    orchestrator = Orchestrator()
    context = orchestrator.run()

    print("\n[OK] Prediction pipeline complete!")
    print(f"[OK] Results exported to: frontend/src/data/predictions.json")
    print(f"[OK] Run the frontend: cd frontend && npm run dev")

    return context


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    main()
