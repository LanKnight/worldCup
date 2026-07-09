import type { PredictionData } from "../../types";

interface SummaryPanelProps {
  data: PredictionData;
}

export function SummaryPanel({ data }: SummaryPanelProps) {
  const champion = data.tournament_predictions[0];

  return (
    <div className="summary-cards">
      <div className="summary-card">
        <div className="label">预测冠军</div>
        <div className="value accent">{champion?.team_name || "—"}</div>
        <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
          {(champion?.champion_prob || 0) * 100}% 概率
        </div>
      </div>

      <div className="summary-card">
        <div className="label">蒙特卡洛模拟次数</div>
        <div className="value accent">{data.monte_carlo_iterations.toLocaleString()}</div>
      </div>

      <div className="summary-card">
        <div className="label">分析球队</div>
        <div className="value accent">{data.teams.length}</div>
      </div>

      <div className="summary-card">
        <div className="label">已预测比赛</div>
        <div className="value accent">{data.match_predictions.length}</div>
      </div>

      <div className="summary-card">
        <div className="label">大模型驱动</div>
        <div className="value accent" style={{ fontSize: "1.2rem" }}>
          DeepSeek API
        </div>
      </div>
    </div>
  );
}
