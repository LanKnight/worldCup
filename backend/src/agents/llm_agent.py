"""
LLM Agent — manages DeepSeek API interactions for tactical analysis and narrative generation.
"""

import json
import logging
from typing import Any

from ..data.database import get_connection
from ..models.llm_analyzer import LLMAnalyzer
from .base import BaseAgent

logger = logging.getLogger(__name__)


class LLMAgent(BaseAgent):
    """DeepSeek LLM analysis and narrative generation agent."""

    def __init__(self, llm_analyzer: LLMAnalyzer):
        super().__init__("LLMAgent")
        self.analyzer = llm_analyzer

    def run(self, context: dict) -> dict:
        """Generate champion analysis narrative using DeepSeek.

        Expects context to contain:
        - 'tournament_predictions': list of TeamTournamentPrediction
        - 'predictions': list of match predictions
        - 'teams': team map
        """
        self.log("Generating champion analysis narrative...")

        if not self.analyzer.client:
            self.warn("DeepSeek API not available — skipping narrative generation.")
            context["llm_narrative"] = "LLM narrative unavailable (DeepSeek API not configured)."
            return context

        tournament_preds = context.get("tournament_predictions", [])
        match_preds = context.get("predictions", [])
        teams = context.get("teams", {})

        # Sort by champion probability
        sorted_preds = sorted(tournament_preds, key=lambda x: x.get("champion_prob", 0), reverse=True)
        top5 = sorted_preds[:5]

        # Build prompt
        top5_text = "\n".join([
            f"{i+1}. {teams.get(p['team_id'], {}).get('name', p['team_id'])} — "
            f"Champion probability: {p['champion_prob']:.1%}, "
            f"Final: {p['final_prob']:.1%}, Semifinal: {p['semi_final_prob']:.1%}"
            for i, p in enumerate(top5)
        ])

        narrative_prompt = f"""You are a World Cup football analyst. Based on statistical model predictions for the 2026 FIFA World Cup (currently at the quarterfinal stage), write a brief analysis of the title contenders.

TOP 5 CHAMPIONSHIP CONTENDERS BY MODEL PROBABILITY:
{top5_text}

QUARTERFINAL PREDICTIONS:
{self._format_match_preds(match_preds, teams)}

Write a 3-4 paragraph analysis covering:
1. The top favorite and why they're favored
2. A dark horse contender
3. Key factors that could determine the champion
4. How this 2026 tournament compares to previous World Cups

Keep it engaging and analytical. Output as plain text (no JSON, no markdown headers)."""

        try:
            response = self.analyzer.client.chat.completions.create(
                model=self.analyzer.model,
                messages=[
                    {"role": "system", "content": "You are a senior World Cup football analyst. Write engaging, insightful analysis."},
                    {"role": "user", "content": narrative_prompt},
                ],
                temperature=0.7,
                max_tokens=800,
            )
            narrative = response.choices[0].message.content.strip()
            self.log("Champion analysis narrative generated successfully.")
        except Exception as e:
            self.warn(f"Failed to generate narrative: {e}")
            narrative = f"Analysis unavailable due to API error: {e}"

        context["llm_narrative"] = narrative
        return context

    def _format_match_preds(self, predictions: list, teams: dict) -> str:
        """Format match predictions for the LLM prompt."""
        lines = []
        for p in predictions[:8]:  # Limit to key matches
            home = teams.get(p["home_team_id"], {}).get("name", p["home_team_id"])
            away = teams.get(p["away_team_id"], {}).get("name", p["away_team_id"])
            lines.append(
                f"- {home} vs {away}: "
                f"Home win {p['home_win_prob']:.1%}, Draw {p['draw_prob']:.1%}, "
                f"Away win {p['away_win_prob']:.1%}"
            )
        return "\n".join(lines)
