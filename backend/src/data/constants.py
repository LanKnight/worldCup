"""
2026 FIFA World Cup hardcoded constants — teams, groups, matches, and results.
Serves as the fallback data source when web scraping fails.

Data current as of: 2026-07-09
Tournament status: Group stage, R32, R16 complete. Quarterfinals in progress.
8 teams remaining: France, Morocco, Spain, Belgium, Norway, England, Argentina, Switzerland
"""

# =============================================================================
# TEAMS — 48 teams in 12 groups (A-L)
# team_id = FIFA country code
# =============================================================================

TEAMS = [
    # Placeholder for TBD matches
    {"id": "TBD", "name": "TBD", "group": "—", "fifa_rank": 0, "elo_rating": 0, "confederation": "—"},
    # Group A
    {"id": "MEX", "name": "Mexico", "group": "A", "fifa_rank": 17, "elo_rating": 1855, "confederation": "CONCACAF"},
    {"id": "RSA", "name": "South Africa", "group": "A", "fifa_rank": 58, "elo_rating": 1530, "confederation": "CAF"},
    {"id": "KOR", "name": "Korea Republic", "group": "A", "fifa_rank": 24, "elo_rating": 1745, "confederation": "AFC"},
    {"id": "CZE", "name": "Czechia", "group": "A", "fifa_rank": 35, "elo_rating": 1680, "confederation": "UEFA"},
    # Group B
    {"id": "SUI", "name": "Switzerland", "group": "B", "fifa_rank": 14, "elo_rating": 1810, "confederation": "UEFA"},
    {"id": "CAN", "name": "Canada", "group": "B", "fifa_rank": 31, "elo_rating": 1720, "confederation": "CONCACAF"},
    {"id": "BIH", "name": "Bosnia & Herzegovina", "group": "B", "fifa_rank": 47, "elo_rating": 1585, "confederation": "UEFA"},
    {"id": "QAT", "name": "Qatar", "group": "B", "fifa_rank": 52, "elo_rating": 1490, "confederation": "AFC"},
    # Group C
    {"id": "BRA", "name": "Brazil", "group": "C", "fifa_rank": 5, "elo_rating": 2075, "confederation": "CONMEBOL"},
    {"id": "MAR", "name": "Morocco", "group": "C", "fifa_rank": 6, "elo_rating": 1880, "confederation": "CAF"},
    {"id": "SCO", "name": "Scotland", "group": "C", "fifa_rank": 28, "elo_rating": 1710, "confederation": "UEFA"},
    {"id": "HAI", "name": "Haiti", "group": "C", "fifa_rank": 86, "elo_rating": 1405, "confederation": "CONCACAF"},
    # Group D
    {"id": "USA", "name": "United States", "group": "D", "fifa_rank": 15, "elo_rating": 1780, "confederation": "CONCACAF"},
    {"id": "AUS", "name": "Australia", "group": "D", "fifa_rank": 27, "elo_rating": 1690, "confederation": "AFC"},
    {"id": "PAR", "name": "Paraguay", "group": "D", "fifa_rank": 50, "elo_rating": 1620, "confederation": "CONMEBOL"},
    {"id": "TUR", "name": "Türkiye", "group": "D", "fifa_rank": 33, "elo_rating": 1735, "confederation": "UEFA"},
    # Group E
    {"id": "GER", "name": "Germany", "group": "E", "fifa_rank": 10, "elo_rating": 1960, "confederation": "UEFA"},
    {"id": "CIV", "name": "Côte d'Ivoire", "group": "E", "fifa_rank": 36, "elo_rating": 1670, "confederation": "CAF"},
    {"id": "ECU", "name": "Ecuador", "group": "E", "fifa_rank": 30, "elo_rating": 1715, "confederation": "CONMEBOL"},
    {"id": "CUW", "name": "Curaçao", "group": "E", "fifa_rank": 91, "elo_rating": 1370, "confederation": "CONCACAF"},
    # Group F
    {"id": "NED", "name": "Netherlands", "group": "F", "fifa_rank": 7, "elo_rating": 1955, "confederation": "UEFA"},
    {"id": "JPN", "name": "Japan", "group": "F", "fifa_rank": 18, "elo_rating": 1800, "confederation": "AFC"},
    {"id": "SWE", "name": "Sweden", "group": "F", "fifa_rank": 25, "elo_rating": 1760, "confederation": "UEFA"},
    {"id": "TUN", "name": "Tunisia", "group": "F", "fifa_rank": 42, "elo_rating": 1580, "confederation": "CAF"},
    # Group G
    {"id": "BEL", "name": "Belgium", "group": "G", "fifa_rank": 8, "elo_rating": 1930, "confederation": "UEFA"},
    {"id": "EGY", "name": "Egypt", "group": "G", "fifa_rank": 32, "elo_rating": 1685, "confederation": "CAF"},
    {"id": "IRN", "name": "IR Iran", "group": "G", "fifa_rank": 22, "elo_rating": 1725, "confederation": "AFC"},
    {"id": "NZL", "name": "New Zealand", "group": "G", "fifa_rank": 95, "elo_rating": 1355, "confederation": "OFC"},
    # Group H
    {"id": "ESP", "name": "Spain", "group": "H", "fifa_rank": 3, "elo_rating": 2040, "confederation": "UEFA"},
    {"id": "CPV", "name": "Cabo Verde", "group": "H", "fifa_rank": 54, "elo_rating": 1515, "confederation": "CAF"},
    {"id": "URU", "name": "Uruguay", "group": "H", "fifa_rank": 16, "elo_rating": 1835, "confederation": "CONMEBOL"},
    {"id": "KSA", "name": "Saudi Arabia", "group": "H", "fifa_rank": 56, "elo_rating": 1475, "confederation": "AFC"},
    # Group I
    {"id": "FRA", "name": "France", "group": "I", "fifa_rank": 1, "elo_rating": 2110, "confederation": "UEFA"},
    {"id": "NOR", "name": "Norway", "group": "I", "fifa_rank": 19, "elo_rating": 1820, "confederation": "UEFA"},
    {"id": "SEN", "name": "Senegal", "group": "I", "fifa_rank": 20, "elo_rating": 1775, "confederation": "CAF"},
    {"id": "IRQ", "name": "Iraq", "group": "I", "fifa_rank": 68, "elo_rating": 1420, "confederation": "AFC"},
    # Group J
    {"id": "ARG", "name": "Argentina", "group": "J", "fifa_rank": 2, "elo_rating": 2095, "confederation": "CONMEBOL"},
    {"id": "AUT", "name": "Austria", "group": "J", "fifa_rank": 26, "elo_rating": 1750, "confederation": "UEFA"},
    {"id": "ALG", "name": "Algeria", "group": "J", "fifa_rank": 37, "elo_rating": 1665, "confederation": "CAF"},
    {"id": "JOR", "name": "Jordan", "group": "J", "fifa_rank": 71, "elo_rating": 1400, "confederation": "AFC"},
    # Group K
    {"id": "COL", "name": "Colombia", "group": "K", "fifa_rank": 9, "elo_rating": 1895, "confederation": "CONMEBOL"},
    {"id": "POR", "name": "Portugal", "group": "K", "fifa_rank": 11, "elo_rating": 1920, "confederation": "UEFA"},
    {"id": "COD", "name": "DR Congo", "group": "K", "fifa_rank": 60, "elo_rating": 1520, "confederation": "CAF"},
    {"id": "UZB", "name": "Uzbekistan", "group": "K", "fifa_rank": 62, "elo_rating": 1435, "confederation": "AFC"},
    # Group L
    {"id": "ENG", "name": "England", "group": "L", "fifa_rank": 4, "elo_rating": 2005, "confederation": "UEFA"},
    {"id": "CRO", "name": "Croatia", "group": "L", "fifa_rank": 13, "elo_rating": 1850, "confederation": "UEFA"},
    {"id": "GHA", "name": "Ghana", "group": "L", "fifa_rank": 43, "elo_rating": 1600, "confederation": "CAF"},
    {"id": "PAN", "name": "Panama", "group": "L", "fifa_rank": 61, "elo_rating": 1445, "confederation": "CONCACAF"},
]

# =============================================================================
# TOURNAMENT MATCHES — All 104 matches with actual/projected results
# Status: completed (C), in_progress (IP), scheduled (S)
# =============================================================================

MATCHES = [
    # ========================
    # GROUP STAGE — 72 matches (all COMPLETED)
    # ========================

    # --- Group A ---
    {"id": "GROUP_A_1", "home_team_id": "MEX", "away_team_id": "RSA", "stage": "group", "group": "A",
     "match_date": "2026-06-11", "venue": "Estadio Azteca", "city": "Mexico City",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_A_2", "home_team_id": "KOR", "away_team_id": "CZE", "stage": "group", "group": "A",
     "match_date": "2026-06-12", "venue": "BMO Field", "city": "Toronto",
     "home_score": 2, "away_score": 1, "status": "completed"},
    {"id": "GROUP_A_3", "home_team_id": "MEX", "away_team_id": "KOR", "stage": "group", "group": "A",
     "match_date": "2026-06-16", "venue": "Estadio Azteca", "city": "Mexico City",
     "home_score": 3, "away_score": 1, "status": "completed"},
    {"id": "GROUP_A_4", "home_team_id": "CZE", "away_team_id": "RSA", "stage": "group", "group": "A",
     "match_date": "2026-06-17", "venue": "BC Place", "city": "Vancouver",
     "home_score": 0, "away_score": 0, "status": "completed"},
    {"id": "GROUP_A_5", "home_team_id": "RSA", "away_team_id": "KOR", "stage": "group", "group": "A",
     "match_date": "2026-06-22", "venue": "BMO Field", "city": "Toronto",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "GROUP_A_6", "home_team_id": "CZE", "away_team_id": "MEX", "stage": "group", "group": "A",
     "match_date": "2026-06-22", "venue": "Estadio Azteca", "city": "Mexico City",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group B ---
    {"id": "GROUP_B_1", "home_team_id": "CAN", "away_team_id": "QAT", "stage": "group", "group": "B",
     "match_date": "2026-06-11", "venue": "BMO Field", "city": "Toronto",
     "home_score": 6, "away_score": 0, "status": "completed"},
    {"id": "GROUP_B_2", "home_team_id": "SUI", "away_team_id": "BIH", "stage": "group", "group": "B",
     "match_date": "2026-06-12", "venue": "BC Place", "city": "Vancouver",
     "home_score": 4, "away_score": 1, "status": "completed"},
    {"id": "GROUP_B_3", "home_team_id": "CAN", "away_team_id": "SUI", "stage": "group", "group": "B",
     "match_date": "2026-06-17", "venue": "BMO Field", "city": "Toronto",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "GROUP_B_4", "home_team_id": "BIH", "away_team_id": "QAT", "stage": "group", "group": "B",
     "match_date": "2026-06-18", "venue": "BC Place", "city": "Vancouver",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_B_5", "home_team_id": "QAT", "away_team_id": "SUI", "stage": "group", "group": "B",
     "match_date": "2026-06-23", "venue": "BMO Field", "city": "Toronto",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "GROUP_B_6", "home_team_id": "BIH", "away_team_id": "CAN", "stage": "group", "group": "B",
     "match_date": "2026-06-23", "venue": "BC Place", "city": "Vancouver",
     "home_score": 1, "away_score": 1, "status": "completed"},

    # --- Group C ---
    {"id": "GROUP_C_1", "home_team_id": "BRA", "away_team_id": "MAR", "stage": "group", "group": "C",
     "match_date": "2026-06-12", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 1, "away_score": 1, "status": "completed"},
    {"id": "GROUP_C_2", "home_team_id": "SCO", "away_team_id": "HAI", "stage": "group", "group": "C",
     "match_date": "2026-06-13", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_C_3", "home_team_id": "BRA", "away_team_id": "SCO", "stage": "group", "group": "C",
     "match_date": "2026-06-17", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "GROUP_C_4", "home_team_id": "HAI", "away_team_id": "MAR", "stage": "group", "group": "C",
     "match_date": "2026-06-18", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 2, "away_score": 4, "status": "completed"},
    {"id": "GROUP_C_5", "home_team_id": "MAR", "away_team_id": "SCO", "stage": "group", "group": "C",
     "match_date": "2026-06-23", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_C_6", "home_team_id": "HAI", "away_team_id": "BRA", "stage": "group", "group": "C",
     "match_date": "2026-06-23", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group D ---
    {"id": "GROUP_D_1", "home_team_id": "USA", "away_team_id": "PAR", "stage": "group", "group": "D",
     "match_date": "2026-06-12", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 4, "away_score": 1, "status": "completed"},
    {"id": "GROUP_D_2", "home_team_id": "AUS", "away_team_id": "TUR", "stage": "group", "group": "D",
     "match_date": "2026-06-13", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "GROUP_D_3", "home_team_id": "USA", "away_team_id": "TUR", "stage": "group", "group": "D",
     "match_date": "2026-06-17", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 2, "away_score": 3, "status": "completed"},
    {"id": "GROUP_D_4", "home_team_id": "AUS", "away_team_id": "PAR", "stage": "group", "group": "D",
     "match_date": "2026-06-18", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "GROUP_D_5", "home_team_id": "PAR", "away_team_id": "TUR", "stage": "group", "group": "D",
     "match_date": "2026-06-23", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "GROUP_D_6", "home_team_id": "AUS", "away_team_id": "USA", "stage": "group", "group": "D",
     "match_date": "2026-06-23", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 1, "away_score": 1, "status": "completed"},

    # --- Group E ---
    {"id": "GROUP_E_1", "home_team_id": "GER", "away_team_id": "CUW", "stage": "group", "group": "E",
     "match_date": "2026-06-13", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 7, "away_score": 1, "status": "completed"},
    {"id": "GROUP_E_2", "home_team_id": "ECU", "away_team_id": "CIV", "stage": "group", "group": "E",
     "match_date": "2026-06-14", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 0, "away_score": 2, "status": "completed"},
    {"id": "GROUP_E_3", "home_team_id": "GER", "away_team_id": "ECU", "stage": "group", "group": "E",
     "match_date": "2026-06-18", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "GROUP_E_4", "home_team_id": "CIV", "away_team_id": "CUW", "stage": "group", "group": "E",
     "match_date": "2026-06-19", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "GROUP_E_5", "home_team_id": "CUW", "away_team_id": "ECU", "stage": "group", "group": "E",
     "match_date": "2026-06-24", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 0, "away_score": 1, "status": "completed"},
    {"id": "GROUP_E_6", "home_team_id": "CIV", "away_team_id": "GER", "stage": "group", "group": "E",
     "match_date": "2026-06-24", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group F ---
    {"id": "GROUP_F_1", "home_team_id": "NED", "away_team_id": "JPN", "stage": "group", "group": "F",
     "match_date": "2026-06-13", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 2, "away_score": 2, "status": "completed"},
    {"id": "GROUP_F_2", "home_team_id": "SWE", "away_team_id": "TUN", "stage": "group", "group": "F",
     "match_date": "2026-06-14", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_F_3", "home_team_id": "NED", "away_team_id": "SWE", "stage": "group", "group": "F",
     "match_date": "2026-06-18", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 5, "away_score": 1, "status": "completed"},
    {"id": "GROUP_F_4", "home_team_id": "TUN", "away_team_id": "JPN", "stage": "group", "group": "F",
     "match_date": "2026-06-19", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 0, "away_score": 4, "status": "completed"},
    {"id": "GROUP_F_5", "home_team_id": "JPN", "away_team_id": "SWE", "stage": "group", "group": "F",
     "match_date": "2026-06-24", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 2, "away_score": 2, "status": "completed"},
    {"id": "GROUP_F_6", "home_team_id": "TUN", "away_team_id": "NED", "stage": "group", "group": "F",
     "match_date": "2026-06-24", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group G ---
    {"id": "GROUP_G_1", "home_team_id": "BEL", "away_team_id": "EGY", "stage": "group", "group": "G",
     "match_date": "2026-06-14", "venue": "Lincoln Financial Field", "city": "Philadelphia",
     "home_score": 1, "away_score": 1, "status": "completed"},
    {"id": "GROUP_G_2", "home_team_id": "IRN", "away_team_id": "NZL", "stage": "group", "group": "G",
     "match_date": "2026-06-15", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "GROUP_G_3", "home_team_id": "BEL", "away_team_id": "NZL", "stage": "group", "group": "G",
     "match_date": "2026-06-19", "venue": "Lincoln Financial Field", "city": "Philadelphia",
     "home_score": 5, "away_score": 1, "status": "completed"},
    {"id": "GROUP_G_4", "home_team_id": "IRN", "away_team_id": "EGY", "stage": "group", "group": "G",
     "match_date": "2026-06-20", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 0, "away_score": 2, "status": "completed"},
    {"id": "GROUP_G_5", "home_team_id": "EGY", "away_team_id": "NZL", "stage": "group", "group": "G",
     "match_date": "2026-06-25", "venue": "Lincoln Financial Field", "city": "Philadelphia",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_G_6", "home_team_id": "IRN", "away_team_id": "BEL", "stage": "group", "group": "G",
     "match_date": "2026-06-25", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 1, "away_score": 1, "status": "completed"},

    # --- Group H ---
    {"id": "GROUP_H_1", "home_team_id": "ESP", "away_team_id": "CPV", "stage": "group", "group": "H",
     "match_date": "2026-06-14", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 0, "away_score": 0, "status": "completed"},
    {"id": "GROUP_H_2", "home_team_id": "URU", "away_team_id": "KSA", "stage": "group", "group": "H",
     "match_date": "2026-06-15", "venue": "BC Place", "city": "Vancouver",
     "home_score": 1, "away_score": 1, "status": "completed"},
    {"id": "GROUP_H_3", "home_team_id": "ESP", "away_team_id": "KSA", "stage": "group", "group": "H",
     "match_date": "2026-06-19", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 4, "away_score": 0, "status": "completed"},
    {"id": "GROUP_H_4", "home_team_id": "URU", "away_team_id": "CPV", "stage": "group", "group": "H",
     "match_date": "2026-06-20", "venue": "BC Place", "city": "Vancouver",
     "home_score": 0, "away_score": 1, "status": "completed"},
    {"id": "GROUP_H_5", "home_team_id": "CPV", "away_team_id": "KSA", "stage": "group", "group": "H",
     "match_date": "2026-06-25", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 1, "away_score": 1, "status": "completed"},
    {"id": "GROUP_H_6", "home_team_id": "URU", "away_team_id": "ESP", "stage": "group", "group": "H",
     "match_date": "2026-06-25", "venue": "BC Place", "city": "Vancouver",
     "home_score": 0, "away_score": 1, "status": "completed"},

    # --- Group I ---
    {"id": "GROUP_I_1", "home_team_id": "FRA", "away_team_id": "SEN", "stage": "group", "group": "I",
     "match_date": "2026-06-15", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 3, "away_score": 1, "status": "completed"},
    {"id": "GROUP_I_2", "home_team_id": "NOR", "away_team_id": "IRQ", "stage": "group", "group": "I",
     "match_date": "2026-06-16", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "GROUP_I_3", "home_team_id": "FRA", "away_team_id": "NOR", "stage": "group", "group": "I",
     "match_date": "2026-06-20", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 4, "away_score": 1, "status": "completed"},
    {"id": "GROUP_I_4", "home_team_id": "IRQ", "away_team_id": "SEN", "stage": "group", "group": "I",
     "match_date": "2026-06-21", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 0, "away_score": 4, "status": "completed"},
    {"id": "GROUP_I_5", "home_team_id": "SEN", "away_team_id": "NOR", "stage": "group", "group": "I",
     "match_date": "2026-06-25", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "GROUP_I_6", "home_team_id": "IRQ", "away_team_id": "FRA", "stage": "group", "group": "I",
     "match_date": "2026-06-25", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 0, "away_score": 5, "status": "completed"},

    # --- Group J ---
    {"id": "GROUP_J_1", "home_team_id": "ARG", "away_team_id": "ALG", "stage": "group", "group": "J",
     "match_date": "2026-06-15", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "GROUP_J_2", "home_team_id": "AUT", "away_team_id": "JOR", "stage": "group", "group": "J",
     "match_date": "2026-06-16", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_J_3", "home_team_id": "ARG", "away_team_id": "AUT", "stage": "group", "group": "J",
     "match_date": "2026-06-20", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_J_4", "home_team_id": "JOR", "away_team_id": "ALG", "stage": "group", "group": "J",
     "match_date": "2026-06-21", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 0, "away_score": 2, "status": "completed"},
    {"id": "GROUP_J_5", "home_team_id": "ALG", "away_team_id": "AUT", "stage": "group", "group": "J",
     "match_date": "2026-06-26", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 3, "away_score": 3, "status": "completed"},
    {"id": "GROUP_J_6", "home_team_id": "JOR", "away_team_id": "ARG", "stage": "group", "group": "J",
     "match_date": "2026-06-26", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group K ---
    {"id": "GROUP_K_1", "home_team_id": "COL", "away_team_id": "POR", "stage": "group", "group": "K",
     "match_date": "2026-06-16", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 0, "away_score": 0, "status": "completed"},
    {"id": "GROUP_K_2", "home_team_id": "COD", "away_team_id": "UZB", "stage": "group", "group": "K",
     "match_date": "2026-06-17", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_K_3", "home_team_id": "COL", "away_team_id": "COD", "stage": "group", "group": "K",
     "match_date": "2026-06-21", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 2, "away_score": 1, "status": "completed"},
    {"id": "GROUP_K_4", "home_team_id": "UZB", "away_team_id": "POR", "stage": "group", "group": "K",
     "match_date": "2026-06-22", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 0, "away_score": 5, "status": "completed"},
    {"id": "GROUP_K_5", "home_team_id": "POR", "away_team_id": "COD", "stage": "group", "group": "K",
     "match_date": "2026-06-26", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "GROUP_K_6", "home_team_id": "UZB", "away_team_id": "COL", "stage": "group", "group": "K",
     "match_date": "2026-06-26", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 0, "away_score": 3, "status": "completed"},

    # --- Group L ---
    {"id": "GROUP_L_1", "home_team_id": "ENG", "away_team_id": "CRO", "stage": "group", "group": "L",
     "match_date": "2026-06-16", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 4, "away_score": 2, "status": "completed"},
    {"id": "GROUP_L_2", "home_team_id": "GHA", "away_team_id": "PAN", "stage": "group", "group": "L",
     "match_date": "2026-06-17", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "GROUP_L_3", "home_team_id": "ENG", "away_team_id": "GHA", "stage": "group", "group": "L",
     "match_date": "2026-06-21", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 0, "away_score": 0, "status": "completed"},
    {"id": "GROUP_L_4", "home_team_id": "PAN", "away_team_id": "CRO", "stage": "group", "group": "L",
     "match_date": "2026-06-22", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 0, "away_score": 3, "status": "completed"},
    {"id": "GROUP_L_5", "home_team_id": "CRO", "away_team_id": "GHA", "stage": "group", "group": "L",
     "match_date": "2026-06-27", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "GROUP_L_6", "home_team_id": "PAN", "away_team_id": "ENG", "stage": "group", "group": "L",
     "match_date": "2026-06-27", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 0, "away_score": 2, "status": "completed"},

    # ========================
    # ROUND OF 32 — 16 matches (all COMPLETED)
    # ========================
    {"id": "R32_1", "home_team_id": "CAN", "away_team_id": "RSA", "stage": "round_of_32",
     "match_date": "2026-06-29", "venue": "BMO Field", "city": "Toronto",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "R32_2", "home_team_id": "BRA", "away_team_id": "JPN", "stage": "round_of_32",
     "match_date": "2026-06-29", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 2, "away_score": 1, "status": "completed"},
    {"id": "R32_3", "home_team_id": "GER", "away_team_id": "PAR", "stage": "round_of_32",
     "match_date": "2026-06-29", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": 1, "away_score": 1, "status": "completed"},  # PAR wins on penalties 4-3
    {"id": "R32_4", "home_team_id": "NED", "away_team_id": "MAR", "stage": "round_of_32",
     "match_date": "2026-06-29", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": 1, "away_score": 1, "status": "completed"},  # MAR wins on penalties 3-2
    {"id": "R32_5", "home_team_id": "FRA", "away_team_id": "SWE", "stage": "round_of_32",
     "match_date": "2026-06-30", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "R32_6", "home_team_id": "CIV", "away_team_id": "NOR", "stage": "round_of_32",
     "match_date": "2026-06-30", "venue": "Levi's Stadium", "city": "Santa Clara",
     "home_score": 1, "away_score": 2, "status": "completed"},
    {"id": "R32_7", "home_team_id": "MEX", "away_team_id": "ECU", "stage": "round_of_32",
     "match_date": "2026-06-30", "venue": "Estadio Azteca", "city": "Mexico City",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "R32_8", "home_team_id": "ENG", "away_team_id": "COD", "stage": "round_of_32",
     "match_date": "2026-07-01", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 2, "away_score": 1, "status": "completed"},
    {"id": "R32_9", "home_team_id": "USA", "away_team_id": "BIH", "stage": "round_of_32",
     "match_date": "2026-07-01", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "R32_10", "home_team_id": "BEL", "away_team_id": "SEN", "stage": "round_of_32",
     "match_date": "2026-07-01", "venue": "Lincoln Financial Field", "city": "Philadelphia",
     "home_score": 3, "away_score": 2, "status": "completed"},  # AET
    {"id": "R32_11", "home_team_id": "ESP", "away_team_id": "AUT", "stage": "round_of_32",
     "match_date": "2026-07-02", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 3, "away_score": 0, "status": "completed"},
    {"id": "R32_12", "home_team_id": "POR", "away_team_id": "CRO", "stage": "round_of_32",
     "match_date": "2026-07-02", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 2, "away_score": 1, "status": "completed"},
    {"id": "R32_13", "home_team_id": "SUI", "away_team_id": "ALG", "stage": "round_of_32",
     "match_date": "2026-07-02", "venue": "BC Place", "city": "Vancouver",
     "home_score": 2, "away_score": 0, "status": "completed"},
    {"id": "R32_14", "home_team_id": "ARG", "away_team_id": "CPV", "stage": "round_of_32",
     "match_date": "2026-07-03", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 3, "away_score": 2, "status": "completed"},  # AET
    {"id": "R32_15", "home_team_id": "COL", "away_team_id": "GHA", "stage": "round_of_32",
     "match_date": "2026-07-03", "venue": "NRG Stadium", "city": "Houston",
     "home_score": 1, "away_score": 0, "status": "completed"},
    {"id": "R32_16", "home_team_id": "AUS", "away_team_id": "EGY", "stage": "round_of_32",
     "match_date": "2026-07-03", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 1, "away_score": 1, "status": "completed"},  # EGY wins on penalties 4-2

    # ========================
    # ROUND OF 16 — 8 matches (all COMPLETED)
    # ========================
    {"id": "R16_1", "home_team_id": "PAR", "away_team_id": "FRA", "stage": "round_of_16",
     "match_date": "2026-07-04", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": 0, "away_score": 1, "status": "completed"},
    {"id": "R16_2", "home_team_id": "CAN", "away_team_id": "MAR", "stage": "round_of_16",
     "match_date": "2026-07-04", "venue": "BMO Field", "city": "Toronto",
     "home_score": 0, "away_score": 3, "status": "completed"},
    {"id": "R16_3", "home_team_id": "BRA", "away_team_id": "NOR", "stage": "round_of_16",
     "match_date": "2026-07-05", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": 1, "away_score": 2, "status": "completed"},  # Major upset!
    {"id": "R16_4", "home_team_id": "MEX", "away_team_id": "ENG", "stage": "round_of_16",
     "match_date": "2026-07-05", "venue": "Estadio Azteca", "city": "Mexico City",
     "home_score": 2, "away_score": 3, "status": "completed"},
    {"id": "R16_5", "home_team_id": "POR", "away_team_id": "ESP", "stage": "round_of_16",
     "match_date": "2026-07-06", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 0, "away_score": 1, "status": "completed"},
    {"id": "R16_6", "home_team_id": "USA", "away_team_id": "BEL", "stage": "round_of_16",
     "match_date": "2026-07-06", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": 1, "away_score": 4, "status": "completed"},
    {"id": "R16_7", "home_team_id": "ARG", "away_team_id": "EGY", "stage": "round_of_16",
     "match_date": "2026-07-07", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": 3, "away_score": 2, "status": "completed"},
    {"id": "R16_8", "home_team_id": "SUI", "away_team_id": "COL", "stage": "round_of_16",
     "match_date": "2026-07-07", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": 0, "away_score": 0, "status": "completed"},  # SUI wins on penalties 4-3

    # ========================
    # QUARTERFINALS — 4 matches (to be predicted)
    # ========================
    {"id": "QF_1", "home_team_id": "FRA", "away_team_id": "MAR", "stage": "quarter_final",
     "match_date": "2026-07-09", "venue": "Gillette Stadium", "city": "Foxborough",
     "home_score": None, "away_score": None, "status": "scheduled"},
    {"id": "QF_2", "home_team_id": "ESP", "away_team_id": "BEL", "stage": "quarter_final",
     "match_date": "2026-07-10", "venue": "SoFi Stadium", "city": "Los Angeles",
     "home_score": None, "away_score": None, "status": "scheduled"},
    {"id": "QF_3", "home_team_id": "NOR", "away_team_id": "ENG", "stage": "quarter_final",
     "match_date": "2026-07-11", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": None, "away_score": None, "status": "scheduled"},
    {"id": "QF_4", "home_team_id": "ARG", "away_team_id": "SUI", "stage": "quarter_final",
     "match_date": "2026-07-11", "venue": "Arrowhead Stadium", "city": "Kansas City",
     "home_score": None, "away_score": None, "status": "scheduled"},

    # ========================
    # SEMIFINALS — 2 matches (to be predicted)
    # ========================
    {"id": "SF_1", "home_team_id": "TBD", "away_team_id": "TBD", "stage": "semi_final",
     "match_date": "2026-07-14", "venue": "AT&T Stadium", "city": "Dallas",
     "home_score": None, "away_score": None, "status": "scheduled"},
    {"id": "SF_2", "home_team_id": "TBD", "away_team_id": "TBD", "stage": "semi_final",
     "match_date": "2026-07-15", "venue": "Mercedes-Benz Stadium", "city": "Atlanta",
     "home_score": None, "away_score": None, "status": "scheduled"},

    # ========================
    # THIRD PLACE — 1 match (to be predicted)
    # ========================
    {"id": "TP_1", "home_team_id": "TBD", "away_team_id": "TBD", "stage": "third_place",
     "match_date": "2026-07-18", "venue": "Hard Rock Stadium", "city": "Miami",
     "home_score": None, "away_score": None, "status": "scheduled"},

    # ========================
    # FINAL — 1 match (to be predicted)
    # ========================
    {"id": "FINAL_1", "home_team_id": "TBD", "away_team_id": "TBD", "stage": "final",
     "match_date": "2026-07-19", "venue": "MetLife Stadium", "city": "East Rutherford",
     "home_score": None, "away_score": None, "status": "scheduled"},
]

# =============================================================================
# KNOCKOUT BRACKET STRUCTURE
# Defines the tree: winner of match X plays winner of match Y in match Z
# =============================================================================

# Quarterfinal bracket: which R16 winners play each other
QF_BRACKET = {
    "QF_1": {"from": ["R16_1", "R16_2"]},  # FRA vs MAR
    "QF_2": {"from": ["R16_5", "R16_6"]},  # ESP vs BEL
    "QF_3": {"from": ["R16_3", "R16_4"]},  # NOR vs ENG
    "QF_4": {"from": ["R16_7", "R16_8"]},  # ARG vs SUI
}

# Semifinal bracket
SF_BRACKET = {
    "SF_1": {"from": ["QF_1", "QF_2"]},  # Winner QF1 vs Winner QF2
    "SF_2": {"from": ["QF_3", "QF_4"]},  # Winner QF3 vs Winner QF4
}

# Third place and Final
FINAL_BRACKET = {
    "TP_1": {"from": ["SF_1", "SF_2"]},   # Losers of semifinals
    "FINAL_1": {"from": ["SF_1", "SF_2"]},  # Winners of semifinals
}

# =============================================================================
# KNOCKOUT RESULTS — actual winners (for completed matches that went to penalties)
# =============================================================================
ACTUAL_KNOCKOUT_WINNERS = {
    "R32_3": "PAR",   # Paraguay beat Germany on penalties
    "R32_4": "MAR",   # Morocco beat Netherlands on penalties
    "R32_10": "BEL",  # Belgium beat Senegal in extra time
    "R32_14": "ARG",  # Argentina beat Cabo Verde in extra time
    "R32_16": "EGY",  # Egypt beat Australia on penalties
    "R16_8": "SUI",   # Switzerland beat Colombia on penalties
    # All other R32/R16 matches decided in 90 minutes
}

# =============================================================================
# STILL ALIVE — Teams still in the tournament
# =============================================================================
ALIVE_TEAMS = {"FRA", "MAR", "ESP", "BEL", "NOR", "ENG", "ARG", "SUI"}

# =============================================================================
# HISTORICAL WORLD CUP WINNERS (for reference)
# =============================================================================
HISTORICAL_CHAMPIONS = [
    {"year": 2022, "winner": "ARG", "runner_up": "FRA"},
    {"year": 2018, "winner": "FRA", "runner_up": "CRO"},
    {"year": 2014, "winner": "GER", "runner_up": "ARG"},
    {"year": 2010, "winner": "ESP", "runner_up": "NED"},
    {"year": 2006, "winner": "ITA", "runner_up": "FRA"},
    {"year": 2002, "winner": "BRA", "runner_up": "GER"},
    {"year": 1998, "winner": "FRA", "runner_up": "BRA"},
]
