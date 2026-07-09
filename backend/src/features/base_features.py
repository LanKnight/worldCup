"""
Base feature computation for match prediction.
Computes ~25 features per match from team data, Elo ratings, and match history.
"""

import math
from collections import defaultdict
from typing import Optional


class FeatureComputer:
    """Computes feature vectors for match prediction."""

    def __init__(self, elo_engine):
        self.elo = elo_engine
        # Cache for team stats
        self._team_stats: dict[str, dict] = defaultdict(lambda: {
            "goals_scored": 0, "goals_conceded": 0, "matches_played": 0,
            "wins": 0, "draws": 0, "losses": 0,
            "clean_sheets": 0, "recent_form": [],  # last 5 results (1=win, 0.5=draw, 0=loss)
        })

    def compute_team_tournament_stats(self, matches: list[dict]) -> None:
        """Compute cumulative tournament statistics for each team from completed matches."""
        for match in matches:
            if match["status"] != "completed":
                continue
            if match["home_score"] is None or match["away_score"] is None:
                continue

            hid = match["home_team_id"]
            aid = match["away_team_id"]
            hs = match["home_score"]
            aw = match["away_score"]

            # Home team stats
            self._team_stats[hid]["goals_scored"] += hs
            self._team_stats[hid]["goals_conceded"] += aw
            self._team_stats[hid]["matches_played"] += 1
            if hs > aw:
                self._team_stats[hid]["wins"] += 1
                self._team_stats[hid]["recent_form"].append(1.0)
            elif hs == aw:
                self._team_stats[hid]["draws"] += 1
                self._team_stats[hid]["recent_form"].append(0.5)
            else:
                self._team_stats[hid]["losses"] += 1
                self._team_stats[hid]["recent_form"].append(0.0)
            if aw == 0:
                self._team_stats[hid]["clean_sheets"] += 1

            # Away team stats
            self._team_stats[aid]["goals_scored"] += aw
            self._team_stats[aid]["goals_conceded"] += hs
            self._team_stats[aid]["matches_played"] += 1
            if aw > hs:
                self._team_stats[aid]["wins"] += 1
                self._team_stats[aid]["recent_form"].append(1.0)
            elif aw == hs:
                self._team_stats[aid]["draws"] += 1
                self._team_stats[aid]["recent_form"].append(0.5)
            else:
                self._team_stats[aid]["losses"] += 1
                self._team_stats[aid]["recent_form"].append(0.0)
            if hs == 0:
                self._team_stats[aid]["clean_sheets"] += 1

        # Keep only last 5 for recent form
        for tid in self._team_stats:
            self._team_stats[tid]["recent_form"] = self._team_stats[tid]["recent_form"][-5:]

    def get_team_features(self, team_id: str, opponent_id: str, stage: str,
                          is_home: bool) -> dict:
        """Compute feature vector for one side of a match."""
        stats = self._team_stats.get(team_id, {})
        opp_stats = self._team_stats.get(opponent_id, {})
        mp = stats.get("matches_played", 0) or 1

        # Team strength features
        elo = self.elo.get_rating(team_id)
        opp_elo = self.elo.get_rating(opponent_id)
        elo_diff = elo - opp_elo

        # Attack/defense features
        avg_goals = stats.get("goals_scored", 0) / mp
        avg_conceded = stats.get("goals_conceded", 0) / mp
        clean_sheet_rate = stats.get("clean_sheets", 0) / mp

        # Form features
        recent = stats.get("recent_form", [])
        last5_pts = sum(recent[-5:]) if recent else 0.0
        last3_pts = sum(recent[-3:]) if recent else 0.0
        win_rate = stats.get("wins", 0) / mp

        # Opponent defense
        opp_avg_conceded = opp_stats.get("goals_conceded", 0) / max(opp_stats.get("matches_played", 1), 1)
        opp_avg_goals = opp_stats.get("goals_scored", 0) / max(opp_stats.get("matches_played", 1), 1)

        # Stage factor
        stage_factors = {
            "group": 1.0, "round_of_32": 1.2, "round_of_16": 1.4,
            "quarter_final": 1.6, "semi_final": 1.8, "third_place": 1.7, "final": 2.0,
        }
        stage_factor = stage_factors.get(stage, 1.0)

        # Home advantage
        home_advantage = 1.0 if is_home else 0.0

        return {
            "elo_rating": elo,
            "elo_diff": elo_diff,
            "avg_goals_scored": avg_goals,
            "avg_goals_conceded": avg_conceded,
            "clean_sheet_rate": clean_sheet_rate,
            "last5_points": last5_pts,
            "last3_points": last3_pts,
            "win_rate": win_rate,
            "matches_played": stats.get("matches_played", 0),
            "stage_factor": stage_factor,
            "home_advantage": home_advantage,
            "opp_avg_goals": opp_avg_goals,
            "opp_avg_conceded": opp_avg_conceded,
        }

    def compute_match_features(self, home_team_id: str, away_team_id: str,
                               stage: str) -> dict:
        """Compute the full feature vector for a match.
        Returns a flat dict with home_ and away_ prefixed features.
        """
        home_feats = self.get_team_features(home_team_id, away_team_id, stage, is_home=True)
        away_feats = self.get_team_features(away_team_id, home_team_id, stage, is_home=False)

        # Combine into flat feature dict
        features = {}
        for k, v in home_feats.items():
            features[f"home_{k}"] = v
        for k, v in away_feats.items():
            features[f"away_{k}"] = v

        # Cross-features
        features["elo_diff"] = home_feats["elo_diff"]  # home - away
        features["form_diff"] = home_feats["last5_points"] - away_feats["last5_points"]
        features["goals_diff"] = home_feats["avg_goals_scored"] - away_feats["avg_goals_conceded"]
        features["stage_factor"] = home_feats["stage_factor"]

        return features

    def compute_stage_difference(self, home_last_match_date: Optional[str],
                                 away_last_match_date: Optional[str]) -> tuple[int, int]:
        """Compute days since last match (fatigue indicator)."""
        # Simplified — returns total matches played as proxy
        return 0, 0  # Placeholder — can be enhanced with actual date parsing
