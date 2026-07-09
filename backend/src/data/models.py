"""
Pydantic data models for the World Cup prediction system.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TournamentStage(str, Enum):
    GROUP = "group"
    ROUND_OF_32 = "round_of_32"
    ROUND_OF_16 = "round_of_16"
    QUARTER_FINAL = "quarter_final"
    SEMI_FINAL = "semi_final"
    THIRD_PLACE = "third_place"
    FINAL = "final"


class Team(BaseModel):
    """A national team participating in the World Cup."""
    id: str = Field(..., description="FIFA country code, e.g. 'ARG', 'FRA'")
    name: str = Field(..., description="Team display name")
    group: str = Field(..., description="Group letter A-L")
    fifa_rank: int = Field(default=0, description="Pre-tournament FIFA ranking")
    elo_rating: float = Field(default=1500.0, description="Current Elo rating")
    confederation: str = Field(default="", description="UEFA, CONMEBOL, etc.")
    market_value: Optional[float] = Field(default=None, description="Total squad market value in EUR")


class Match(BaseModel):
    """A World Cup match."""
    id: str = Field(..., description="Unique match ID, e.g. 'GROUP_A_1', 'R32_1'")
    home_team_id: str
    away_team_id: str
    stage: TournamentStage
    group: Optional[str] = Field(default=None, description="Group letter if group stage")
    match_date: Optional[datetime] = None
    venue: Optional[str] = None
    city: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: MatchStatus = MatchStatus.SCHEDULED


class MatchPrediction(BaseModel):
    """Prediction for a single match."""
    match_id: str
    home_team_id: str
    away_team_id: str
    home_win_prob: float = Field(ge=0, le=1)
    draw_prob: float = Field(ge=0, le=1)
    away_win_prob: float = Field(ge=0, le=1)
    predicted_home_goals: float = Field(ge=0)
    predicted_away_goals: float = Field(ge=0)
    elo_home_win_prob: Optional[float] = None
    poisson_home_win_prob: Optional[float] = None
    lightgbm_home_win_prob: Optional[float] = None
    llm_correction: Optional[float] = Field(default=0.0, ge=-0.05, le=0.05)
    llm_narrative: Optional[str] = None
    model_version: str = "1.0.0"


class TeamTournamentPrediction(BaseModel):
    """Tournament-level prediction for a team."""
    team_id: str
    team_name: str
    champion_prob: float = Field(ge=0, le=1)
    final_prob: float = Field(ge=0, le=1)
    semi_final_prob: float = Field(ge=0, le=1)
    quarter_final_prob: float = Field(ge=0, le=1)
    round_of_16_prob: float = Field(ge=0, le=1)
    avg_goals_scored: float = Field(default=0.0)
    avg_goals_conceded: float = Field(default=0.0)


class PredictionExport(BaseModel):
    """Top-level export structure for the frontend."""
    generated_at: str
    model_version: str
    monte_carlo_iterations: int
    teams: list[Team]
    matches: list[Match]
    match_predictions: list[MatchPrediction]
    tournament_predictions: list[TeamTournamentPrediction]
