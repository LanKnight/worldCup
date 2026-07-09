import type { PredictionData } from "../../types";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface ChampionOddsProps {
  data: PredictionData;
}

const COLORS = ["#3b82f6", "#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#7c3aed", "#2563eb", "#4f46e5"];

export function ChampionOdds({ data }: ChampionOddsProps) {
  const top10 = data.tournament_predictions.slice(0, 10);

  const chartData = top10.map(tp => ({
    name: tp.team_name,
    probability: +(tp.champion_prob * 100).toFixed(1),
    team_id: tp.team_id,
  }));

  return (
    <div className="odds-container">
      <div className="odds-chart">
        <h2>夺冠概率 — Top 10 球队</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 80, right: 30, top: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis type="number" domain={[0, 25]} tick={{ fill: "var(--text-muted)", fontSize: 12 }} unit="%" />
            <YAxis type="category" dataKey="name" tick={{ fill: "var(--text)", fontSize: 13 }} width={75} />
            <Tooltip
              contentStyle={{
                background: "var(--bg-card)",
                border: "1px solid var(--border)",
                borderRadius: 8,
                color: "var(--text)",
              }}
              formatter={(value) => [`${value}%`, "夺冠概率"]}
            />
            <Bar dataKey="probability" radius={[0, 4, 4, 0]}>
              {chartData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="champion-cards">
        {data.tournament_predictions.slice(0, 8).map((tp, i) => (
          <div key={tp.team_id} className="champion-card">
            <div className="team-name" style={{ color: COLORS[i] }}>
              #{i + 1} {tp.team_name}
            </div>
            <div className="champion-pct">{(tp.champion_prob * 100).toFixed(1)}%</div>
            <div className="stage-probs">
              <span>四强 <strong>{(tp.quarter_final_prob * 100).toFixed(0)}%</strong></span>
              <span>决赛 <strong>{(tp.final_prob * 100).toFixed(0)}%</strong></span>
              <span>半决赛 <strong>{(tp.semi_final_prob * 100).toFixed(0)}%</strong></span>
              <span>场均进球 <strong>{tp.avg_goals_scored?.toFixed(1)}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
