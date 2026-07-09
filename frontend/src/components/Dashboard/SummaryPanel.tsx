import type { PredictionData } from "../../types";

interface SummaryPanelProps {
  data: PredictionData;
}

export function SummaryPanel({ data }: SummaryPanelProps) {
  const champion = data.tournament_predictions[0];

  return (
    <div className="summary-cards">
      <div className="summary-card">
        <div className="label">Predicted Champion</div>
        <div className="value accent">{champion?.team_name || "—"}</div>
        <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
          {(champion?.champion_prob || 0) * 100}% probability
        </div>
      </div>

      <div className="summary-card">
        <div className="label">Monte Carlo Simulations</div>
        <div className="value accent">{data.monte_carlo_iterations.toLocaleString()}</div>
      </div>

      <div className="summary-card">
        <div className="label">Teams Analyzed</div>
        <div className="value accent">{data.teams.length}</div>
      </div>

      <div className="summary-card">
        <div className="label">Matches Predicted</div>
        <div className="value accent">{data.match_predictions.length}</div>
      </div>

      <div className="summary-card">
        <div className="label">Powered by LLM</div>
        <div className="value accent" style={{ fontSize: "1.2rem" }}>
          DeepSeek API
        </div>
      </div>
    </div>
  );
}
