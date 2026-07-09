"""
LightGBM model for match outcome prediction.
Trained on 2014-2022 World Cup data + 2026 completed matches.
"""

import logging
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV

from ..config import LGB_PARAMS, DATA_PROCESSED

logger = logging.getLogger(__name__)


class LightGBMModel:
    """LightGBM-based match predictor with classifier + goal regressor."""

    def __init__(self):
        self.classifier: LGBMClassifier | None = None
        self.home_goal_regressor: LGBMRegressor | None = None
        self.away_goal_regressor: LGBMRegressor | None = None
        self._feature_columns: list[str] = []
        self._is_fitted = False

    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract feature matrix, excluding non-feature columns."""
        exclude = {"match_id", "outcome", "home_goals", "away_goals"}
        feature_cols = [c for c in df.columns if c not in exclude]
        self._feature_columns = feature_cols
        return df[feature_cols].fillna(0).values

    def train(self, df: pd.DataFrame) -> dict:
        """Train LightGBM models on historical data.
        df must contain 'outcome' (0=home win, 1=draw, 2=away win)
        and optionally 'home_goals'/'away_goals' columns.
        """
        if "outcome" not in df.columns:
            raise ValueError("DataFrame must contain 'outcome' column")

        X = self._prepare_features(df)
        y_cls = df["outcome"].values.astype(int)

        # --- Classifier ---
        cls_params = {
            "max_depth": LGB_PARAMS["max_depth"],
            "num_leaves": LGB_PARAMS["num_leaves"],
            "min_data_in_leaf": LGB_PARAMS["min_data_in_leaf"],
            "learning_rate": LGB_PARAMS["learning_rate"],
            "n_estimators": LGB_PARAMS["n_estimators"],
            "reg_alpha": LGB_PARAMS["reg_alpha"],
            "reg_lambda": LGB_PARAMS["reg_lambda"],
            "subsample": LGB_PARAMS["subsample"],
            "colsample_bytree": LGB_PARAMS["colsample_bytree"],
            "random_state": LGB_PARAMS["random_state"],
            "objective": "multiclass",
            "num_class": 3,
            "verbose": -1,
        }
        self.classifier = LGBMClassifier(**cls_params)
        self.classifier.fit(X, y_cls)

        # --- Goal Regressors ---
        if "home_goals" in df.columns and "away_goals" in df.columns:
            reg_params = {
                "max_depth": LGB_PARAMS["max_depth"],
                "num_leaves": LGB_PARAMS["num_leaves"],
                "min_data_in_leaf": LGB_PARAMS["min_data_in_leaf"],
                "learning_rate": LGB_PARAMS["learning_rate"],
                "n_estimators": LGB_PARAMS["n_estimators"],
                "reg_alpha": LGB_PARAMS["reg_alpha"],
                "reg_lambda": LGB_PARAMS["reg_lambda"],
                "subsample": LGB_PARAMS["subsample"],
                "colsample_bytree": LGB_PARAMS["colsample_bytree"],
                "random_state": LGB_PARAMS["random_state"],
                "objective": "regression",
                "verbose": -1,
            }

            y_home_goals = df["home_goals"].values
            y_away_goals = df["away_goals"].values

            self.home_goal_regressor = LGBMRegressor(**reg_params)
            self.home_goal_regressor.fit(X, y_home_goals)

            self.away_goal_regressor = LGBMRegressor(**reg_params)
            self.away_goal_regressor.fit(X, y_away_goals)

        self._is_fitted = True

        # Compute training accuracy
        train_pred = self.classifier.predict(X)
        accuracy = (train_pred == y_cls).mean()

        logger.info(f"LightGBM trained: {len(X)} samples, {len(self._feature_columns)} features, "
                     f"train accuracy: {accuracy:.3f}")

        return {"samples": len(X), "features": len(self._feature_columns), "train_accuracy": accuracy}

    def predict(self, features_df: pd.DataFrame) -> dict:
        """Predict match outcome for new data."""
        if not self._is_fitted:
            raise RuntimeError("Model must be trained before prediction")

        X = features_df[self._feature_columns].fillna(0).values

        # Class probabilities
        proba = self.classifier.predict_proba(X)
        home_win = float(proba[0, 0])
        draw = float(proba[0, 1])
        away_win = float(proba[0, 2])

        # Goal predictions
        home_goals = away_goals = None
        if self.home_goal_regressor is not None:
            home_goals = float(self.home_goal_regressor.predict(X)[0])
            home_goals = max(0.0, home_goals)
        if self.away_goal_regressor is not None:
            away_goals = float(self.away_goal_regressor.predict(X)[0])
            away_goals = max(0.0, away_goals)

        return {
            "model": "lightgbm",
            "home_win_prob": home_win,
            "draw_prob": draw,
            "away_win_prob": away_win,
            "predicted_home_goals": round(home_goals, 2) if home_goals is not None else None,
            "predicted_away_goals": round(away_goals, 2) if away_goals is not None else None,
        }

    def save(self, path: Path) -> None:
        """Save model to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "classifier": self.classifier,
                "home_goal_regressor": self.home_goal_regressor,
                "away_goal_regressor": self.away_goal_regressor,
                "feature_columns": self._feature_columns,
                "is_fitted": self._is_fitted,
            }, f)
        logger.info(f"Model saved to {path}")

    def load(self, path: Path) -> None:
        """Load model from disk."""
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.classifier = data["classifier"]
        self.home_goal_regressor = data["home_goal_regressor"]
        self.away_goal_regressor = data["away_goal_regressor"]
        self._feature_columns = data["feature_columns"]
        self._is_fitted = data["is_fitted"]
        logger.info(f"Model loaded from {path}")
