import type { TournamentPrediction } from "../../types";

interface TopContendersProps {
  contenders: TournamentPrediction[];
}

export function TopContenders({ contenders }: TopContendersProps) {
  const top8 = contenders.slice(0, 8);

  return (
    <div className="contender-list">
      {top8.map((tp, i) => (
        <div key={tp.team_id} className="contender-row">
          <span className="contender-rank">#{i + 1}</span>
          <span className="contender-name">{tp.team_name}</span>
          <div className="contender-bar-wrapper">
            <div
              className={`contender-bar ${i < 3 ? "high" : i < 6 ? "medium" : "low"}`}
              style={{ width: `${tp.champion_prob * 100}%` }}
            >
              <span className="contender-pct">{(tp.champion_prob * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
