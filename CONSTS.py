

YEARS_TO_SEASON_IDS = {year:id for (year,id) in zip([str(i) for i in range(2007,2024)], [str(i) for i in range(304,321)])}

PLAYER_COLUMNS = [
            "Rank",
            "Player",
            "Team",
            "Position",
            "Value",
            "Split",
            "Year"
        ]

PLAYER_SPLITS = [
             "", #empty for "all games"
             "home",
             "away",
             "conference",
             "last_2_weeks",
             "last_4_weeks",
             "top_50"
         ]

TEAM_COLUMNS = [
            "Rank",
            "Team",
            "CurrentSeason",
            "Last3",
            "Last1",
            "Home",
            "Away",
            "PreviousSeason"
            "Date"
        ]
