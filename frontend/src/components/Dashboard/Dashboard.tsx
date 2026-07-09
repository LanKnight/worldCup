import type { PredictionData } from "../../types";
import { SummaryPanel } from "./SummaryPanel";

interface DashboardProps {
  data: PredictionData;
}

export function Dashboard({ data }: DashboardProps) {
  const top8 = data.tournament_predictions.slice(0, 8);

  return (
    <div className="dashboard">
      <SummaryPanel data={data} />

      <div className="dashboard-grid">
        <div className="panel">
          <h2>Championship Contenders</h2>
          <div className="contender-list">
            {top8.map((tp, i) => (
              <div key={tp.team_id} className="contender-row">
                <span className="contender-rank">#{i + 1}</span>
                <span className="contender-name">{tp.team_name}</span>
                <div className="contender-bar-wrapper">
                  <div
                    className={`contender-bar ${i < 3 ? "high" : i < 6 ? "medium" : "low"}`}
                    style={{ width: `${Math.max(tp.champion_prob * 100, 2)}%` }}
                  >
                    <span className="contender-pct">
                      {(tp.champion_prob * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>Quarterfinal Predictions</h2>
          {data.match_predictions.map(pred => {
            const home = data.teams.find(t => t.id === pred.home_team_id);
            const away = data.teams.find(t => t.id === pred.away_team_id);
            return (
              <div key={pred.match_id} className="match-card" style={{ marginBottom: 10 }}>
                <div className="team-row">
                  <span className="team-name">{home?.name || pred.home_team_id}</span>
                  <span className="team-score">{pred.predicted_home_goals.toFixed(1)}</span>
                </div>
                <div className="team-row">
                  <span className="team-name">{away?.name || pred.away_team_id}</span>
                  <span className="team-score">{pred.predicted_away_goals.toFixed(1)}</span>
                </div>
                <div className="prob-row">
                  <span className="prob home">H {(pred.home_win_prob * 100).toFixed(0)}%</span>
                  <span className="prob draw">D {(pred.draw_prob * 100).toFixed(0)}%</span>
                  <span className="prob away">A {(pred.away_win_prob * 100).toFixed(0)}%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {data.llm_narrative && (
        <div className="narrative">
          <h2>AI-Powered DeepSeek LLM Analysis</h2>
          <p>{data.llm_narrative}</p>
        </div>
      )}
    </div>
  );
}
