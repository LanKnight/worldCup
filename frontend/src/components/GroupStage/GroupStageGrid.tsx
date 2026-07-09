import type { PredictionData } from "../../types";

interface GroupStageGridProps {
  data: PredictionData;
}

export function GroupStageGrid({ data }: GroupStageGridProps) {
  // Group matches and teams by group
  const groups = new Map<string, {
    teams: Array<{ id: string; name: string; pts: number; gd: number; gs: number; played: number }>;
    matches: typeof data.matches;
  }>();

  // Initialize groups
  const groupLetters = "ABCDEFGHIJKL".split("");
  for (const g of groupLetters) {
    groups.set(g, { teams: [], matches: [] });
  }

  // Group matches
  for (const match of data.matches) {
    if (match.stage === "group" && match.group) {
      const g = groups.get(match.group);
      if (g) g.matches.push(match);
    }
  }

  // Compute standings for each group
  for (const [_groupName, groupData] of groups) {
    const teamStats = new Map<string, { pts: number; gd: number; gs: number; played: number }>();

    for (const match of groupData.matches) {
      if (!match.home_score || !match.away_score) continue;

      for (const tid of [match.home_team_id, match.away_team_id]) {
        if (!teamStats.has(tid)) {
          teamStats.set(tid, { pts: 0, gd: 0, gs: 0, played: 0 });
        }
      }

      const hs = teamStats.get(match.home_team_id)!;
      const as = teamStats.get(match.away_team_id)!;

      hs.played++; as.played++;
      hs.gd += match.home_score - match.away_score;
      as.gd += match.away_score - match.home_score;
      hs.gs += match.home_score;
      as.gs += match.away_score;

      if (match.home_score > match.away_score) { hs.pts += 3; }
      else if (match.away_score > match.home_score) { as.pts += 3; }
      else { hs.pts += 1; as.pts += 1; }
    }

    // Create team list with sort
    groupData.teams = Array.from(teamStats.entries())
      .map(([id, stats]) => ({
        id,
        name: data.teams.find(t => t.id === id)?.name || id,
        pts: stats.pts,
        gd: stats.gd,
        gs: stats.gs,
        played: stats.played,
      }))
      .sort((a, b) => b.pts - a.pts || b.gd - a.gd || b.gs - a.gs);
  }

  return (
    <div>
      <div className="panel" style={{ marginBottom: 24 }}>
        <h2>Group Stage Results</h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
          48 teams, 12 groups. Top 2 from each group + 8 best 3rd-place teams advanced to Round of 32.
          Green dots indicate teams that advanced.
        </p>
      </div>

      <div className="group-grid">
        {Array.from(groups.entries()).map(([groupName, groupData]) => (
          <div key={groupName} className="group-table">
            <h3>Group {groupName}</h3>
            <table>
              <thead>
                <tr>
                  <th>Team</th>
                  <th>P</th>
                  <th>W/D/L</th>
                  <th>GD</th>
                  <th>Pts</th>
                </tr>
              </thead>
              <tbody>
                {groupData.teams.map((team, i) => (
                  <tr key={team.id} className={i < 2 ? "qualified" : ""}>
                    <td>{team.name}</td>
                    <td>{team.played}</td>
                    <td style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                      {team.pts > 0 ? `${Math.floor(team.pts / 3)}/${Math.floor((team.pts % 3))}/${team.played - Math.floor(team.pts / 3) - Math.floor((team.pts % 3))}` : `0/0/${team.played}`}
                    </td>
                    <td style={{ color: team.gd > 0 ? "var(--green)" : team.gd < 0 ? "var(--red)" : "var(--text-muted)" }}>
                      {team.gd > 0 ? "+" : ""}{team.gd}
                    </td>
                    <td style={{ fontWeight: 700 }}>{team.pts}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
