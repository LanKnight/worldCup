"""
Historical World Cup match results (2014, 2018, 2022) for model training.
Each record: home_team_id, away_team_id, home_score, away_score, stage
"""

HISTORICAL_MATCHES = [
    # ========================
    # 2022 FIFA World Cup — Qatar (64 matches)
    # ========================
    # Group A
    {"home_team_id": "QAT", "away_team_id": "ECU", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "SEN", "away_team_id": "NED", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "QAT", "away_team_id": "SEN", "home_score": 1, "away_score": 3, "stage": "group", "year": 2022},
    {"home_team_id": "NED", "away_team_id": "ECU", "home_score": 1, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "NED", "away_team_id": "QAT", "home_score": 2, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "ECU", "away_team_id": "SEN", "home_score": 1, "away_score": 2, "stage": "group", "year": 2022},
    # Group B
    {"home_team_id": "ENG", "away_team_id": "IRN", "home_score": 6, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "USA", "away_team_id": "WAL", "home_score": 1, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "WAL", "away_team_id": "IRN", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "ENG", "away_team_id": "USA", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "IRN", "away_team_id": "USA", "home_score": 0, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "WAL", "away_team_id": "ENG", "home_score": 0, "away_score": 3, "stage": "group", "year": 2022},
    # Group C
    {"home_team_id": "ARG", "away_team_id": "KSA", "home_score": 1, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "MEX", "away_team_id": "POL", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "POL", "away_team_id": "KSA", "home_score": 2, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "ARG", "away_team_id": "MEX", "home_score": 2, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "KSA", "away_team_id": "MEX", "home_score": 1, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "POL", "away_team_id": "ARG", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    # Group D
    {"home_team_id": "FRA", "away_team_id": "AUS", "home_score": 4, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "DEN", "away_team_id": "TUN", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "TUN", "away_team_id": "AUS", "home_score": 0, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "FRA", "away_team_id": "DEN", "home_score": 2, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "AUS", "away_team_id": "DEN", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "TUN", "away_team_id": "FRA", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    # Group E
    {"home_team_id": "GER", "away_team_id": "JPN", "home_score": 1, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "ESP", "away_team_id": "CRC", "home_score": 7, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "JPN", "away_team_id": "CRC", "home_score": 0, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "ESP", "away_team_id": "GER", "home_score": 1, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "CRC", "away_team_id": "GER", "home_score": 2, "away_score": 4, "stage": "group", "year": 2022},
    {"home_team_id": "JPN", "away_team_id": "ESP", "home_score": 2, "away_score": 1, "stage": "group", "year": 2022},
    # Group F
    {"home_team_id": "MAR", "away_team_id": "CRO", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "BEL", "away_team_id": "CAN", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "BEL", "away_team_id": "MAR", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "CRO", "away_team_id": "CAN", "home_score": 4, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "CAN", "away_team_id": "MAR", "home_score": 1, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "CRO", "away_team_id": "BEL", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    # Group G
    {"home_team_id": "SUI", "away_team_id": "CMR", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "BRA", "away_team_id": "SRB", "home_score": 2, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "CMR", "away_team_id": "SRB", "home_score": 3, "away_score": 3, "stage": "group", "year": 2022},
    {"home_team_id": "BRA", "away_team_id": "SUI", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "CMR", "away_team_id": "BRA", "home_score": 1, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "SRB", "away_team_id": "SUI", "home_score": 2, "away_score": 3, "stage": "group", "year": 2022},
    # Group H
    {"home_team_id": "URU", "away_team_id": "KOR", "home_score": 0, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "POR", "away_team_id": "GHA", "home_score": 3, "away_score": 2, "stage": "group", "year": 2022},
    {"home_team_id": "KOR", "away_team_id": "GHA", "home_score": 2, "away_score": 3, "stage": "group", "year": 2022},
    {"home_team_id": "POR", "away_team_id": "URU", "home_score": 2, "away_score": 0, "stage": "group", "year": 2022},
    {"home_team_id": "KOR", "away_team_id": "POR", "home_score": 2, "away_score": 1, "stage": "group", "year": 2022},
    {"home_team_id": "GHA", "away_team_id": "URU", "home_score": 0, "away_score": 2, "stage": "group", "year": 2022},
    # R16 2022
    {"home_team_id": "NED", "away_team_id": "USA", "home_score": 3, "away_score": 1, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "ARG", "away_team_id": "AUS", "home_score": 2, "away_score": 1, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "FRA", "away_team_id": "POL", "home_score": 3, "away_score": 1, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "ENG", "away_team_id": "SEN", "home_score": 3, "away_score": 0, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "JPN", "away_team_id": "CRO", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "BRA", "away_team_id": "KOR", "home_score": 4, "away_score": 1, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "MAR", "away_team_id": "ESP", "home_score": 0, "away_score": 0, "stage": "round_of_16", "year": 2022},
    {"home_team_id": "POR", "away_team_id": "SUI", "home_score": 6, "away_score": 1, "stage": "round_of_16", "year": 2022},
    # QF 2022
    {"home_team_id": "NED", "away_team_id": "ARG", "home_score": 2, "away_score": 2, "stage": "quarter_final", "year": 2022},
    {"home_team_id": "CRO", "away_team_id": "BRA", "home_score": 1, "away_score": 1, "stage": "quarter_final", "year": 2022},
    {"home_team_id": "ENG", "away_team_id": "FRA", "home_score": 1, "away_score": 2, "stage": "quarter_final", "year": 2022},
    {"home_team_id": "MAR", "away_team_id": "POR", "home_score": 1, "away_score": 0, "stage": "quarter_final", "year": 2022},
    # SF 2022
    {"home_team_id": "ARG", "away_team_id": "CRO", "home_score": 3, "away_score": 0, "stage": "semi_final", "year": 2022},
    {"home_team_id": "FRA", "away_team_id": "MAR", "home_score": 2, "away_score": 0, "stage": "semi_final", "year": 2022},
    # 3rd 2022
    {"home_team_id": "CRO", "away_team_id": "MAR", "home_score": 2, "away_score": 1, "stage": "third_place", "year": 2022},
    # Final 2022
    {"home_team_id": "ARG", "away_team_id": "FRA", "home_score": 3, "away_score": 3, "stage": "final", "year": 2022},

    # ========================
    # 2018 FIFA World Cup — Russia (64 matches)
    # ========================
    # Group A
    {"home_team_id": "RUS", "away_team_id": "KSA", "home_score": 5, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "EGY", "away_team_id": "URU", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "RUS", "away_team_id": "EGY", "home_score": 3, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "URU", "away_team_id": "KSA", "home_score": 1, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "KSA", "away_team_id": "EGY", "home_score": 2, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "URU", "away_team_id": "RUS", "home_score": 3, "away_score": 0, "stage": "group", "year": 2018},
    # Group B
    {"home_team_id": "MAR", "away_team_id": "IRN", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "POR", "away_team_id": "ESP", "home_score": 3, "away_score": 3, "stage": "group", "year": 2018},
    {"home_team_id": "POR", "away_team_id": "MAR", "home_score": 1, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "IRN", "away_team_id": "ESP", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "ESP", "away_team_id": "MAR", "home_score": 2, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "IRN", "away_team_id": "POR", "home_score": 1, "away_score": 1, "stage": "group", "year": 2018},
    # Group C
    {"home_team_id": "FRA", "away_team_id": "AUS", "home_score": 2, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "PER", "away_team_id": "DEN", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "FRA", "away_team_id": "PER", "home_score": 1, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "DEN", "away_team_id": "AUS", "home_score": 1, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "AUS", "away_team_id": "PER", "home_score": 0, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "DEN", "away_team_id": "FRA", "home_score": 0, "away_score": 0, "stage": "group", "year": 2018},
    # Group D
    {"home_team_id": "ARG", "away_team_id": "ISL", "home_score": 1, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "CRO", "away_team_id": "NGA", "home_score": 2, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "ARG", "away_team_id": "CRO", "home_score": 0, "away_score": 3, "stage": "group", "year": 2018},
    {"home_team_id": "NGA", "away_team_id": "ISL", "home_score": 2, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "ISL", "away_team_id": "CRO", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "NGA", "away_team_id": "ARG", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    # Group E
    {"home_team_id": "CRC", "away_team_id": "SRB", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "BRA", "away_team_id": "SUI", "home_score": 1, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "BRA", "away_team_id": "CRC", "home_score": 2, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "SRB", "away_team_id": "SUI", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "CRC", "away_team_id": "SUI", "home_score": 2, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "SRB", "away_team_id": "BRA", "home_score": 0, "away_score": 2, "stage": "group", "year": 2018},
    # Group F
    {"home_team_id": "GER", "away_team_id": "MEX", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "SWE", "away_team_id": "KOR", "home_score": 1, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "GER", "away_team_id": "SWE", "home_score": 2, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "KOR", "away_team_id": "MEX", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "KOR", "away_team_id": "GER", "home_score": 2, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "MEX", "away_team_id": "SWE", "home_score": 0, "away_score": 3, "stage": "group", "year": 2018},
    # Group G
    {"home_team_id": "BEL", "away_team_id": "PAN", "home_score": 3, "away_score": 0, "stage": "group", "year": 2018},
    {"home_team_id": "TUN", "away_team_id": "ENG", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "BEL", "away_team_id": "TUN", "home_score": 5, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "ENG", "away_team_id": "PAN", "home_score": 6, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "ENG", "away_team_id": "BEL", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "PAN", "away_team_id": "TUN", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    # Group H
    {"home_team_id": "COL", "away_team_id": "JPN", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "POL", "away_team_id": "SEN", "home_score": 1, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "JPN", "away_team_id": "SEN", "home_score": 2, "away_score": 2, "stage": "group", "year": 2018},
    {"home_team_id": "POL", "away_team_id": "COL", "home_score": 0, "away_score": 3, "stage": "group", "year": 2018},
    {"home_team_id": "JPN", "away_team_id": "POL", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    {"home_team_id": "SEN", "away_team_id": "COL", "home_score": 0, "away_score": 1, "stage": "group", "year": 2018},
    # R16 2018
    {"home_team_id": "FRA", "away_team_id": "ARG", "home_score": 4, "away_score": 3, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "URU", "away_team_id": "POR", "home_score": 2, "away_score": 1, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "ESP", "away_team_id": "RUS", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "CRO", "away_team_id": "DEN", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "BRA", "away_team_id": "MEX", "home_score": 2, "away_score": 0, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "BEL", "away_team_id": "JPN", "home_score": 3, "away_score": 2, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "SWE", "away_team_id": "SUI", "home_score": 1, "away_score": 0, "stage": "round_of_16", "year": 2018},
    {"home_team_id": "COL", "away_team_id": "ENG", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2018},
    # QF 2018
    {"home_team_id": "URU", "away_team_id": "FRA", "home_score": 0, "away_score": 2, "stage": "quarter_final", "year": 2018},
    {"home_team_id": "BRA", "away_team_id": "BEL", "home_score": 1, "away_score": 2, "stage": "quarter_final", "year": 2018},
    {"home_team_id": "SWE", "away_team_id": "ENG", "home_score": 0, "away_score": 2, "stage": "quarter_final", "year": 2018},
    {"home_team_id": "RUS", "away_team_id": "CRO", "home_score": 2, "away_score": 2, "stage": "quarter_final", "year": 2018},
    # SF 2018
    {"home_team_id": "FRA", "away_team_id": "BEL", "home_score": 1, "away_score": 0, "stage": "semi_final", "year": 2018},
    {"home_team_id": "CRO", "away_team_id": "ENG", "home_score": 2, "away_score": 1, "stage": "semi_final", "year": 2018},
    # 3rd 2018
    {"home_team_id": "BEL", "away_team_id": "ENG", "home_score": 2, "away_score": 0, "stage": "third_place", "year": 2018},
    # Final 2018
    {"home_team_id": "FRA", "away_team_id": "CRO", "home_score": 4, "away_score": 2, "stage": "final", "year": 2018},

    # ========================
    # 2014 FIFA World Cup — Brazil (64 matches)
    # ========================
    # Group A
    {"home_team_id": "BRA", "away_team_id": "CRO", "home_score": 3, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "MEX", "away_team_id": "CMR", "home_score": 1, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "BRA", "away_team_id": "MEX", "home_score": 0, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "CMR", "away_team_id": "CRO", "home_score": 0, "away_score": 4, "stage": "group", "year": 2014},
    {"home_team_id": "CMR", "away_team_id": "BRA", "home_score": 1, "away_score": 4, "stage": "group", "year": 2014},
    {"home_team_id": "CRO", "away_team_id": "MEX", "home_score": 1, "away_score": 3, "stage": "group", "year": 2014},
    # Group B
    {"home_team_id": "ESP", "away_team_id": "NED", "home_score": 1, "away_score": 5, "stage": "group", "year": 2014},
    {"home_team_id": "CHI", "away_team_id": "AUS", "home_score": 3, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "AUS", "away_team_id": "NED", "home_score": 2, "away_score": 3, "stage": "group", "year": 2014},
    {"home_team_id": "ESP", "away_team_id": "CHI", "home_score": 0, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "AUS", "away_team_id": "ESP", "home_score": 0, "away_score": 3, "stage": "group", "year": 2014},
    {"home_team_id": "NED", "away_team_id": "CHI", "home_score": 2, "away_score": 0, "stage": "group", "year": 2014},
    # Group C
    {"home_team_id": "COL", "away_team_id": "GRE", "home_score": 3, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "CIV", "away_team_id": "JPN", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "COL", "away_team_id": "CIV", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "JPN", "away_team_id": "GRE", "home_score": 0, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "JPN", "away_team_id": "COL", "home_score": 1, "away_score": 4, "stage": "group", "year": 2014},
    {"home_team_id": "GRE", "away_team_id": "CIV", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    # Group D
    {"home_team_id": "URU", "away_team_id": "CRC", "home_score": 1, "away_score": 3, "stage": "group", "year": 2014},
    {"home_team_id": "ENG", "away_team_id": "ITA", "home_score": 1, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "URU", "away_team_id": "ENG", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "ITA", "away_team_id": "CRC", "home_score": 0, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "CRC", "away_team_id": "ENG", "home_score": 0, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "ITA", "away_team_id": "URU", "home_score": 0, "away_score": 1, "stage": "group", "year": 2014},
    # Group E
    {"home_team_id": "SUI", "away_team_id": "ECU", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "FRA", "away_team_id": "HON", "home_score": 3, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "SUI", "away_team_id": "FRA", "home_score": 2, "away_score": 5, "stage": "group", "year": 2014},
    {"home_team_id": "HON", "away_team_id": "ECU", "home_score": 1, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "ECU", "away_team_id": "FRA", "home_score": 0, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "HON", "away_team_id": "SUI", "home_score": 0, "away_score": 3, "stage": "group", "year": 2014},
    # Group F
    {"home_team_id": "ARG", "away_team_id": "BIH", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "IRN", "away_team_id": "NGA", "home_score": 0, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "ARG", "away_team_id": "IRN", "home_score": 1, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "NGA", "away_team_id": "BIH", "home_score": 1, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "BIH", "away_team_id": "IRN", "home_score": 3, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "NGA", "away_team_id": "ARG", "home_score": 2, "away_score": 3, "stage": "group", "year": 2014},
    # Group G
    {"home_team_id": "GER", "away_team_id": "POR", "home_score": 4, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "GHA", "away_team_id": "USA", "home_score": 1, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "GER", "away_team_id": "GHA", "home_score": 2, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "USA", "away_team_id": "POR", "home_score": 2, "away_score": 2, "stage": "group", "year": 2014},
    {"home_team_id": "POR", "away_team_id": "GHA", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "USA", "away_team_id": "GER", "home_score": 0, "away_score": 1, "stage": "group", "year": 2014},
    # Group H
    {"home_team_id": "BEL", "away_team_id": "ALG", "home_score": 2, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "RUS", "away_team_id": "KOR", "home_score": 1, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "BEL", "away_team_id": "RUS", "home_score": 1, "away_score": 0, "stage": "group", "year": 2014},
    {"home_team_id": "KOR", "away_team_id": "ALG", "home_score": 2, "away_score": 4, "stage": "group", "year": 2014},
    {"home_team_id": "ALG", "away_team_id": "RUS", "home_score": 1, "away_score": 1, "stage": "group", "year": 2014},
    {"home_team_id": "KOR", "away_team_id": "BEL", "home_score": 0, "away_score": 1, "stage": "group", "year": 2014},
    # R16 2014
    {"home_team_id": "BRA", "away_team_id": "CHI", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "COL", "away_team_id": "URU", "home_score": 2, "away_score": 0, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "FRA", "away_team_id": "NGA", "home_score": 2, "away_score": 0, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "GER", "away_team_id": "ALG", "home_score": 2, "away_score": 1, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "NED", "away_team_id": "MEX", "home_score": 2, "away_score": 1, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "CRC", "away_team_id": "GRE", "home_score": 1, "away_score": 1, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "ARG", "away_team_id": "SUI", "home_score": 1, "away_score": 0, "stage": "round_of_16", "year": 2014},
    {"home_team_id": "BEL", "away_team_id": "USA", "home_score": 2, "away_score": 1, "stage": "round_of_16", "year": 2014},
    # QF 2014
    {"home_team_id": "FRA", "away_team_id": "GER", "home_score": 0, "away_score": 1, "stage": "quarter_final", "year": 2014},
    {"home_team_id": "BRA", "away_team_id": "COL", "home_score": 2, "away_score": 1, "stage": "quarter_final", "year": 2014},
    {"home_team_id": "ARG", "away_team_id": "BEL", "home_score": 1, "away_score": 0, "stage": "quarter_final", "year": 2014},
    {"home_team_id": "NED", "away_team_id": "CRC", "home_score": 0, "away_score": 0, "stage": "quarter_final", "year": 2014},
    # SF 2014
    {"home_team_id": "BRA", "away_team_id": "GER", "home_score": 1, "away_score": 7, "stage": "semi_final", "year": 2014},
    {"home_team_id": "NED", "away_team_id": "ARG", "home_score": 0, "away_score": 0, "stage": "semi_final", "year": 2014},
    # 3rd 2014
    {"home_team_id": "BRA", "away_team_id": "NED", "home_score": 0, "away_score": 3, "stage": "third_place", "year": 2014},
    # Final 2014
    {"home_team_id": "GER", "away_team_id": "ARG", "home_score": 1, "away_score": 0, "stage": "final", "year": 2014},
]
