import type { Match, MatchPrediction, Team } from "../../types";

interface BracketMatchProps {
  match: Match;
  prediction?: MatchPrediction;
  teamMap: Map<string, Team>;
  isPending?: boolean;
}

export function BracketMatch({ match, prediction, teamMap, isPending }: BracketMatchProps) {
  const home = teamMap.get(match.home_team_id);
  const away = teamMap.get(match.away_team_id);
  const isCompleted = match.status === "completed";

  const homeIsWinner = isCompleted && match.home_score != null && match.away_score != null
    && match.home_score > match.away_score;
  const awayIsWinner = isCompleted && match.home_score != null && match.away_score != null
    && match.away_score > match.home_score;

  return (
    <div className="match-card" style={isPending ? { opacity: 0.5 } : undefined}>
      {isPending ? (
        <div style={{ textAlign: "center", color: "var(--text-muted)", padding: 12 }}>
          {match.stage === "semi_final" ? "Winner QF1/2" : match.stage === "final" ? "TBD" : "TBD"}
          <div style={{ fontSize: "0.7rem" }}>vs</div>
          {match.stage === "semi_final" ? "Winner QF3/4" : match.stage === "final" ? "TBD" : "TBD"}
        </div>
      ) : (
        <>
          <div className={`team-row ${homeIsWinner ? "winner" : ""}`}>
            <span className="team-name">{home?.name || match.home_team_id}</span>
            {isCompleted && <span className="team-score">{match.home_score}</span>}
          </div>
          <div className={`team-row ${awayIsWinner ? "winner" : ""}`}>
            <span className="team-name">{away?.name || match.away_team_id}</span>
            {isCompleted && <span className="team-score">{match.away_score}</span>}
          </div>
          {prediction && !isCompleted && (
            <div className="prob-row">
              <span className="prob home" title="Home win">H {(prediction?.home_win_prob || 0) * 100 | 0}%</span>
              <span className="prob draw" title="Draw">D {(prediction?.draw_prob || 0) * 100 | 0}%</span>
              <span className="prob away" title="Away win">A {(prediction?.away_win_prob || 0) * 100 | 0}%</span>
            </div>
          )}
          {!prediction && isCompleted && (
            <div className="prob-row" style={{ justifyContent: "center" }}>
              <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>
                {match.match_date}
              </span>
            </div>
          )}
        </>
      )}
    </div>
  );
}
