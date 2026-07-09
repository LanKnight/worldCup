"""
DeepSeek LLM integration for tactical analysis and prediction correction.
Uses OpenAI-compatible API to call DeepSeek, outputting structured JSON correction factors.

Key principle: LLM does NOT predict match scores directly.
It only outputs tactical advantage assessment (±5% correction).
"""

import json
import logging
import re
from typing import Optional

from openai import OpenAI

from ..config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a world-class football (soccer) tactical analyst. Your role is to analyze World Cup matchups and provide structured tactical assessments.

CRITICAL RULES:
1. You do NOT predict match scores or outcomes directly.
2. You ONLY output a structured JSON object with tactical analysis.
3. Your correction factor must be between -0.05 and +0.05 (max ±5% adjustment).
4. Base your analysis on: team form, tactical style matchup, key player status, historical patterns, and tournament context.

OUTPUT FORMAT (strict JSON, no markdown, no extra text):
{
  "tactical_advantage": "home" | "away" | "neutral",
  "correction_factor": <float between -0.05 and 0.05>,
  "key_factors": ["factor1", "factor2", "factor3"],
  "confidence": "high" | "medium" | "low",
  "narrative": "<2-3 sentence tactical analysis in English>"
}

CORRECTION FACTOR GUIDELINES:
- +0.05: Heavy tactical advantage for home team (style mismatch, key opponent injuries, etc.)
- +0.02 to +0.03: Slight tactical advantage
- 0.00: Genuinely balanced matchup
- -0.02 to -0.03: Slight tactical disadvantage for home team
- -0.05: Heavy tactical disadvantage for home team

Only use ±0.05 in extreme cases with very high confidence."""


def _build_match_prompt(home_team: str, away_team: str, stage: str,
                        home_elo: float, away_elo: float,
                        elo_win_prob: float, home_form: str, away_form: str,
                        home_tournament_goals: float, away_tournament_goals: float,
                        head_to_head_note: str = "") -> str:
    """Build a detailed prompt for the LLM tactical analysis."""

    elo_diff = home_elo - away_elo
    favorite = home_team if elo_diff > 0 else away_team
    underdog = away_team if elo_diff > 0 else home_team

    prompt = f"""Analyze this 2026 FIFA World Cup {stage} match:

MATCH: {home_team} (Home) vs {away_team} (Away)

TEAM STRENGTHS:
- {home_team}: Elo rating {home_elo:.0f}, tournament goals/game {home_tournament_goals:.1f}
- {away_team}: Elo rating {away_elo:.0f}, tournament goals/game {away_tournament_goals:.1f}
- Elo difference: {abs(elo_diff):.0f} points favoring {favorite}
- Base Elo win probability for {home_team}: {elo_win_prob:.1%}

RECENT FORM:
- {home_team}: {home_form}
- {away_team}: {away_form}
{f'- Head-to-head context: {head_to_head_note}' if head_to_head_note else ''}

TOURNAMENT CONTEXT:
- Stage: {stage}
- Winner advances to the {'semi-final' if 'quarter' in stage else 'next round'}
- This is a single-elimination knockout match

TASK: Analyze the tactical matchup. Consider playing styles, key players (Messi for Argentina, Mbappé for France, Haaland for Norway, Kane for England, etc.), tournament momentum, and any tactical mismatches. Output ONLY the JSON object."""
    return prompt


class LLMAnalyzer:
    """DeepSeek-powered tactical analysis and prediction correction engine."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.base_url = base_url or DEEPSEEK_BASE_URL

        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not set. LLM analysis will be simulated.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        self.model = DEEPSEEK_MODEL

    def analyze_match(self, home_team: str, away_team: str, stage: str,
                      home_elo: float, away_elo: float,
                      elo_win_prob: float,
                      home_form: str = "No data",
                      away_form: str = "No data",
                      home_goals: float = 0.0,
                      away_goals: float = 0.0,
                      head_to_head: str = "") -> dict:
        """Run tactical analysis via DeepSeek API.
        Returns structured correction factor dict.
        """

        prompt = _build_match_prompt(
            home_team=home_team, away_team=away_team, stage=stage,
            home_elo=home_elo, away_elo=away_elo,
            elo_win_prob=elo_win_prob,
            home_form=home_form, away_form=away_form,
            home_tournament_goals=home_goals, away_tournament_goals=away_goals,
            head_to_head_note=head_to_head,
        )

        if self.client is None:
            # Simulation mode: return neutral assessment
            return self._simulate_analysis(home_team, away_team, home_elo, away_elo)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # Low temperature for consistency
                max_tokens=500,
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from response (handle potential markdown wrapping)
            result = self._parse_json_response(content)

            # Validate correction factor range
            cf = result.get("correction_factor", 0.0)
            if abs(cf) > 0.05:
                logger.warning(f"LLM correction factor {cf} out of range, clamping.")
                cf = max(-0.05, min(0.05, cf))
                result["correction_factor"] = cf

            logger.info(
                f"LLM analysis: {home_team} vs {away_team} → "
                f"advantage={result.get('tactical_advantage')}, cf={cf:+.3f}"
            )

            return result

        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            return self._simulate_analysis(home_team, away_team, home_elo, away_elo)

    def _parse_json_response(self, content: str) -> dict:
        """Extract and parse JSON from LLM response (handles markdown code blocks)."""
        # Try to find JSON block in markdown
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if json_match:
            content = json_match.group(1)

        # Try direct parse
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Extract first JSON-like structure
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

        logger.warning(f"Failed to parse LLM response as JSON: {content[:200]}")
        return self._default_response()

    def _default_response(self) -> dict:
        return {
            "tactical_advantage": "neutral",
            "correction_factor": 0.0,
            "key_factors": ["insufficient data for analysis"],
            "confidence": "low",
            "narrative": "Unable to generate tactical analysis.",
        }

    def _simulate_analysis(self, home_team: str, away_team: str,
                           home_elo: float, away_elo: float) -> dict:
        """Generate simulated analysis when DeepSeek API is unavailable."""
        elo_diff = home_elo - away_elo

        # Simple heuristic based on Elo difference
        if abs(elo_diff) < 50:
            advantage = "neutral"
            cf = 0.0
        elif elo_diff > 0:
            advantage = "home"
            cf = min(0.03, elo_diff / 10000)
        else:
            advantage = "away"
            cf = max(-0.03, elo_diff / 10000)

        return {
            "tactical_advantage": advantage,
            "correction_factor": round(cf, 4),
            "key_factors": ["Elo rating differential", "tournament form", "simulated analysis (API unavailable)"],
            "confidence": "low",
            "narrative": f"Simulated analysis: {home_team} {'has' if elo_diff > 0 else 'does not have'} "
                         f"a tactical edge over {away_team} based on Elo ratings and tournament performance.",
        }
