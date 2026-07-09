export interface Team {
  id: string;
  name: string;
  group: string;
  fifa_rank: number;
  elo_rating: number;
  confederation: string;
}

export interface Match {
  id: string;
  home_team_id: string;
  away_team_id: string;
  stage: string;
  group?: string;
  match_date?: string;
  venue?: string;
  city?: string;
  home_score?: number;
  away_score?: number;
  status: "scheduled" | "in_progress" | "completed";
}

export interface MatchPrediction {
  match_id: string;
  home_team_id: string;
  away_team_id: string;
  home_win_prob: number;
  draw_prob: number;
  away_win_prob: number;
  predicted_home_goals: number;
  predicted_away_goals: number;
  elo_home_win_prob?: number;
  poisson_home_win_prob?: number;
  lightgbm_home_win_prob?: number;
  llm_correction?: number;
  llm_narrative?: string;
  model_version: string;
}

export interface TournamentPrediction {
  team_id: string;
  team_name: string;
  champion_prob: number;
  final_prob: number;
  semi_final_prob: number;
  quarter_final_prob: number;
  round_of_16_prob: number;
  avg_goals_scored: number;
  avg_goals_conceded: number;
}

export interface PredictionData {
  generated_at: string;
  model_version: string;
  monte_carlo_iterations: number;
  teams: Team[];
  matches: Match[];
  match_predictions: MatchPrediction[];
  tournament_predictions: TournamentPrediction[];
  llm_narrative?: string;
}
