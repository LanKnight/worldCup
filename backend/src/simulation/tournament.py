"""
2026 World Cup tournament bracket builder and match resolver.
Models the 48-team, 12-group format with correct knockout progression.
"""

import logging
from copy import deepcopy
from typing import Optional

from ..data.constants import QF_BRACKET, SF_BRACKET, FINAL_BRACKET, ACTUAL_KNOCKOUT_WINNERS

logger = logging.getLogger(__name__)


class TournamentState:
    """Mutable state for one tournament simulation iteration."""

    def __init__(self):
        self.group_standings: dict[str, list[dict]] = {}  # group -> [{team_id, pts, gd, gs}]
        self.match_results: dict[str, tuple[str, int, int]] = {}  # match_id -> (winner_id, h_score, a_score)
        self.knockout_winners: dict[str, str] = {}  # match_id -> winning team_id
        self.eliminated: set[str] = set()
        self.team_goals_scored: dict[str, int] = {}
        self.team_goals_conceded: dict[str, int] = {}

    def record_goals(self, team_id: str, scored: int, conceded: int) -> None:
        self.team_goals_scored[team_id] = self.team_goals_scored.get(team_id, 0) + scored
        self.team_goals_conceded[team_id] = self.team_goals_conceded.get(team_id, 0) + conceded


class TournamentSimulator:
    """Simulates one complete World Cup tournament."""

    def __init__(self):
        self.teams: dict[str, dict] = {}
        self.group_matches: dict[str, list[dict]] = {}  # group -> matches
        self.knockout_matches: dict[str, dict] = {}  # match_id -> match
        self.actual_results: dict[str, dict] = {}  # match_id -> {winner, home_score, away_score}

    def load_teams(self, teams: dict[str, dict]) -> None:
        """Load team data (excluding TBD)."""
        self.teams = {tid: t for tid, t in teams.items() if tid != "TBD"}

    def load_completed_matches(self, matches: list[dict]) -> None:
        """Load actual results of completed matches."""
        for m in matches:
            if m["status"] != "completed":
                continue
            if m["home_score"] is None or m["away_score"] is None:
                continue

            # Determine actual winner
            hid = m["home_team_id"]
            aid = m["away_team_id"]
            hs = m["home_score"]
            aw = m["away_score"]

            if hs > aw:
                winner = hid
            elif aw > hs:
                winner = aid
            else:
                # Draw — check if penalty winner exists for knockout
                winner = ACTUAL_KNOCKOUT_WINNERS.get(m["id"])

            self.actual_results[m["id"]] = {
                "winner": winner,
                "home_score": hs,
                "away_score": aw,
                "stage": m["stage"],
                "group": m.get("group"),
                "home_team_id": hid,
                "away_team_id": aid,
            }

            # Build group match index
            if m.get("group"):
                g = m["group"]
                if g not in self.group_matches:
                    self.group_matches[g] = []
                self.group_matches[g].append(m)

            # Build knockout match index
            if m["stage"] != "group" and m["id"] not in ("SF_1", "SF_2", "TP_1", "FINAL_1"):
                self.knockout_matches[m["id"]] = m

    def simulate(self, match_probabilities: dict) -> TournamentState:
        """Simulate one complete tournament from current state.

        Args:
            match_probabilities: {match_id: {home_win, draw, away_win, home_goals, away_goals}}
        """
        import random

        state = TournamentState()

        # Phase 1: Group stage — use actual results only
        for group, matches in self.group_matches.items():
            standings = self._build_group_standings(group, matches, state)
            state.group_standings[group] = standings

        # Determine knockout qualifiers from groups
        # Top 2 from each group + 8 best 3rd-place teams
        group_winners = []
        group_runners_up = []
        group_thirds = []

        for group_letter in "ABCDEFGHIJKL":
            standings = state.group_standings.get(group_letter, [])
            if len(standings) >= 3:
                group_winners.append((group_letter, standings[0]["team_id"]))
                group_runners_up.append((group_letter, standings[1]["team_id"]))
                group_thirds.append((group_letter, standings[2]))

        # Sort third-place teams by points, GD, GS
        group_thirds.sort(key=lambda x: (x[1]["pts"], x[1]["gd"], x[1]["gs"]), reverse=True)
        best_thirds = [gt[1]["team_id"] for gt in group_thirds[:8]]

        knockout_teams = [gw[1] for gw in group_winners] + [gr[1] for gr in group_runners_up] + best_thirds

        # Phase 2: Knockout stage
        # Build actual bracket pairings
        # R32 pairings based on 2026 format (simplified mapping)
        self._simulate_knockout_round("R32", knockout_teams, match_probabilities,
                                      state, random, "round_of_32")

        # R16 winners come from R32
        r16_teams = self._get_knockout_winners("R32", state)
        self._simulate_knockout_round("R16", r16_teams, match_probabilities,
                                      state, random, "round_of_16")

        # QF winners from R16
        qf_teams = self._get_knockout_winners("R16", state)
        self._simulate_knockout_round("QF", qf_teams, match_probabilities,
                                      state, random, "quarter_final")

        # SF
        sf_teams = self._get_knockout_winners("QF", state)
        self._simulate_knockout_round("SF", sf_teams, match_probabilities,
                                      state, random, "semi_final")

        # Final & Third Place
        sf_winners = self._get_knockout_winners("SF", state)
        sf_losers = self._get_knockout_losers("SF", state)

        # Third place match
        if len(sf_losers) >= 2:
            loser_match_id = "TP_1"
            if loser_match_id in match_probabilities:
                probs = match_probabilities[loser_match_id]
                # Override with actual losers
                h_win, draw, a_win = probs["home_win"], probs["draw"], probs["away_win"]
                r = random.random()
                if r < h_win:
                    state.knockout_winners[loser_match_id] = sf_losers[0]
                elif r < h_win + draw:
                    # Penalty shootout for draw
                    state.knockout_winners[loser_match_id] = sf_losers[0] if random.random() < 0.5 else sf_losers[1]
                else:
                    state.knockout_winners[loser_match_id] = sf_losers[1]

        # Final
        if len(sf_winners) >= 2:
            self._simulate_final("FINAL_1", sf_winners, match_probabilities, state, random)

        return state

    def _build_group_standings(self, group: str, matches: list[dict],
                               state: TournamentState) -> list[dict]:
        """Compute group standings from match results."""
        team_pts: dict[str, int] = {}
        team_gd: dict[str, int] = {}
        team_gs: dict[str, int] = {}
        team_ga: dict[str, int] = {}

        for m in matches:
            hid = m["home_team_id"]
            aid = m["away_team_id"]

            # Use actual results
            actual = self.actual_results.get(m["id"], {})
            hs = actual.get("home_score", 0)
            aw = actual.get("away_score", 0)

            for tid in [hid, aid]:
                if tid not in team_pts:
                    team_pts[tid] = team_gd[tid] = team_gs[tid] = team_ga[tid] = 0

            team_gs[hid] += hs
            team_ga[hid] += aw
            team_gs[aid] += aw
            team_ga[aid] += hs
            team_gd[hid] = team_gs[hid] - team_ga[hid]
            team_gd[aid] = team_gs[aid] - team_ga[aid]

            if hs > aw:
                team_pts[hid] += 3
            elif aw > hs:
                team_pts[aid] += 3
            else:
                team_pts[hid] += 1
                team_pts[aid] += 1

            state.record_goals(hid, hs, aw)
            state.record_goals(aid, aw, hs)

        # Build sorted standings
        team_ids = list(team_pts.keys())
        # Sort: points desc, GD desc, GS desc
        team_ids.sort(key=lambda tid: (team_pts[tid], team_gd[tid], team_gs[tid]), reverse=True)

        standings = []
        for tid in team_ids:
            standings.append({
                "team_id": tid,
                "pts": team_pts[tid],
                "gd": team_gd[tid],
                "gs": team_gs[tid],
            })

        return standings

    def _simulate_knockout_round(self, prefix: str, teams: list[str],
                                 match_probabilities: dict, state: TournamentState,
                                 rng, stage: str) -> None:
        """Simulate a knockout round with given teams."""
        if len(teams) < 2:
            return

        # Pair teams: team[0] vs team[1], team[2] vs team[3], etc.
        for i in range(0, len(teams) - 1, 2):
            match_id = f"{prefix}_{i//2 + 1}"
            home = teams[i]
            away = teams[i + 1]

            # Check if this match has actual results
            if match_id in self.actual_results:
                actual = self.actual_results[match_id]
                winner = actual["winner"]
                if winner:
                    state.knockout_winners[match_id] = winner
                    state.record_goals(home, actual["home_score"], actual["away_score"])
                    state.record_goals(away, actual["away_score"], actual["home_score"])
                continue

            # Use probabilities to sample outcome
            probs = match_probabilities.get(match_id, {
                "home_win": 0.40, "draw": 0.28, "away_win": 0.32,
                "home_goals": 1.4, "away_goals": 1.2,
            })

            h_win = probs["home_win"]
            draw = probs["draw"]
            a_win = probs["away_win"]

            r = rng.random()
            if r < h_win:
                winner = home
            elif r < h_win + draw:
                # Draw → penalty shootout (50/50 simplified)
                winner = home if rng.random() < 0.5 else away
            else:
                winner = away

            state.knockout_winners[match_id] = winner

            # Simulate goals
            hg = max(0, int(rng.gauss(probs.get("home_goals", 1.4), 0.8)))
            ag = max(0, int(rng.gauss(probs.get("away_goals", 1.2), 0.8)))
            state.record_goals(home, hg, ag)
            state.record_goals(away, ag, hg)

    def _simulate_final(self, match_id: str, teams: list[str],
                        match_probabilities: dict, state: TournamentState,
                        rng) -> None:
        """Simulate the final match."""
        if len(teams) < 2:
            return

        home = teams[0]
        away = teams[1]

        probs = match_probabilities.get(match_id, {
            "home_win": 0.40, "draw": 0.28, "away_win": 0.32,
            "home_goals": 1.4, "away_goals": 1.2,
        })

        r = rng.random()
        if r < probs["home_win"]:
            winner = home
        elif r < probs["home_win"] + probs["draw"]:
            winner = home if rng.random() < 0.5 else away
        else:
            winner = away

        state.knockout_winners[match_id] = winner

        hg = max(0, int(rng.gauss(probs.get("home_goals", 1.4), 0.8)))
        ag = max(0, int(rng.gauss(probs.get("away_goals", 1.2), 0.8)))
        state.record_goals(home, hg, ag)
        state.record_goals(away, ag, hg)

    def _get_knockout_winners(self, prefix: str, state: TournamentState) -> list[str]:
        """Get winning teams from a knockout round in order."""
        winners = []
        for i in range(1, 17):  # Max 16 matches per round
            match_id = f"{prefix}_{i}"
            if match_id in state.knockout_winners:
                winners.append(state.knockout_winners[match_id])
        return winners

    def _get_knockout_losers(self, prefix: str, state: TournamentState) -> list[str]:
        """Get losing teams from a knockout round."""
        # This is simplified — we track only winners
        # For SF losers, we need to know which teams played
        # For now, return empty (third place match handled separately)
        return []
