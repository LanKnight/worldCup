"""
Central configuration for the World Cup prediction system.
"""

import os
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"
DATA_PREDICTIONS = DATA_DIR / "predictions"
DB_PATH = DATA_DIR / "worldcup.db"
FRONTEND_DATA_DIR = PROJECT_ROOT / "frontend" / "src" / "data"

# Ensure directories exist
for d in [DATA_RAW, DATA_PROCESSED, DATA_PREDICTIONS, FRONTEND_DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- DeepSeek API ---
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# --- Elo Configuration ---
ELO_K_FACTOR = 40           # World Cup weight
ELO_INITIAL = 1500          # Default starting Elo
ELO_HOME_ADVANTAGE = 100    # Elo points for home advantage

# --- Poisson Configuration ---
POISSON_MAX_GOALS = 10      # Max goals considered in score probability matrix

# --- LightGBM Configuration ---
LGB_PARAMS = {
    "max_depth": 4,
    "num_leaves": 16,
    "min_data_in_leaf": 10,
    "learning_rate": 0.05,
    "n_estimators": 200,
    "reg_alpha": 0.1,
    "reg_lambda": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}

# --- Ensemble Weights ---
ENSEMBLE_WEIGHTS = {
    "group_stage": {
        "elo": 0.25,
        "poisson": 0.25,
        "lightgbm": 0.40,
        "llm": 0.10,
    },
    "knockout": {
        "elo": 0.20,
        "poisson": 0.20,
        "lightgbm": 0.45,
        "llm": 0.15,
    },
}

# --- Monte Carlo ---
MC_ITERATIONS = 5000
MC_RANDOM_SEED = 42

# --- Tournament Stages ---
STAGE_WEIGHTS = {
    "group": 1.0,
    "round_of_32": 1.2,
    "round_of_16": 1.4,
    "quarter_final": 1.6,
    "semi_final": 1.8,
    "final": 2.0,
}

# --- 2026 World Cup Specific ---
WORLD_CUP_YEAR = 2026
N_TEAMS = 48
N_GROUPS = 12
TEAMS_PER_GROUP = 4
TOTAL_MATCHES = 104  # 72 group + 32 knockout
