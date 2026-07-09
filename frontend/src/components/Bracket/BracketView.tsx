import type { PredictionData } from "../../types";
import { BracketMatch } from "./BracketMatch";

interface BracketViewProps {
  data: PredictionData;
}

export function BracketView({ data }: BracketViewProps) {
  const teamMap = new Map(data.teams.map(t => [t.id, t]));
  const predMap = new Map(data.match_predictions.map(p => [p.match_id, p]));

  const getMatch = (id: string) => data.matches.find(m => m.id === id);
  const getPred = (id: string) => predMap.get(id);

  const qfMatches = ["QF_1", "QF_2", "QF_3", "QF_4"].map(id => {
    const match = getMatch(id);
    const pred = getPred(id);
    return { match, pred };
  });

  const sfMatches = ["SF_1", "SF_2"].map(id => {
    const match = getMatch(id);
    return { match, pred: null };
  });

  const finalMatch = getMatch("FINAL_1");

  return (
    <div>
      <div className="panel" style={{ marginBottom: 24 }}>
        <h2>2026世界杯淘汰赛对阵图</h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
          8支球队进入1/4决赛。预测基于 Elo + 泊松 + LightGBM + DeepSeek 大模型四引擎融合。
        </p>
      </div>

      <div className="bracket-container">
        <div className="bracket-rounds">
          {/* 1/4决赛 */}
          <div className="bracket-round">
            <h3>1/4 决赛</h3>
            {qfMatches.map(({ match, pred }) => (
              match ? (
                <BracketMatch
                  key={match.id}
                  match={match}
                  prediction={pred || undefined}
                  teamMap={teamMap}
                />
              ) : null
            ))}
          </div>

          {/* 半决赛 */}
          <div className="bracket-round" style={{ justifyContent: "center" }}>
            <h3>半决赛</h3>
            {sfMatches.map(({ match }) => (
              match ? (
                <BracketMatch
                  key={match.id}
                  match={match}
                  teamMap={teamMap}
                  isPending={true}
                />
              ) : null
            ))}
          </div>

          {/* 决赛 */}
          <div className="bracket-round" style={{ justifyContent: "center" }}>
            <h3>决赛</h3>
            {finalMatch && (
              <BracketMatch
                match={finalMatch}
                teamMap={teamMap}
                isPending={true}
              />
            )}
          </div>
        </div>
      </div>

      {/* 晋级概率表 */}
      <div className="panel" style={{ marginTop: 24 }}>
        <h2>各阶段晋级概率</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.85rem" }}>
            <thead>
              <tr style={{ color: "var(--text-muted)", textAlign: "left" }}>
                <th style={{ padding: 8 }}>球队</th>
                <th style={{ padding: 8, textAlign: "center" }}>四强</th>
                <th style={{ padding: 8, textAlign: "center" }}>半决赛</th>
                <th style={{ padding: 8, textAlign: "center" }}>决赛</th>
                <th style={{ padding: 8, textAlign: "center" }}>夺冠</th>
              </tr>
            </thead>
            <tbody>
              {data.tournament_predictions.filter(tp => tp.champion_prob > 0.01).map(tp => (
                <tr key={tp.team_id} style={{ borderBottom: "1px solid var(--border)" }}>
                  <td style={{ padding: 8, fontWeight: 600 }}>{tp.team_name}</td>
                  <td style={{ padding: 8, textAlign: "center" }}>
                    <div style={{
                      width: `${tp.quarter_final_prob * 100}%`,
                      height: 6, background: "var(--accent)", borderRadius: 3, opacity: 0.7,
                    }} />
                    {(tp.quarter_final_prob * 100).toFixed(0)}%
                  </td>
                  <td style={{ padding: 8, textAlign: "center" }}>
                    <div style={{
                      width: `${tp.semi_final_prob * 100}%`,
                      height: 6, background: "#6366f1", borderRadius: 3, opacity: 0.7,
                    }} />
                    {(tp.semi_final_prob * 100).toFixed(0)}%
                  </td>
                  <td style={{ padding: 8, textAlign: "center" }}>
                    <div style={{
                      width: `${tp.final_prob * 100}%`,
                      height: 6, background: "#8b5cf6", borderRadius: 3, opacity: 0.7,
                    }} />
                    {(tp.final_prob * 100).toFixed(0)}%
                  </td>
                  <td style={{ padding: 8, textAlign: "center", fontWeight: 700, color: "var(--accent)" }}>
                    {(tp.champion_prob * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
