
SEASON_IDS_TO_YEARS = {year:id for (year,id) in zip([str(i) for i in range(304,321)], [str(i) for i in range(2007,2024)])}

PLAYER_COLUMNS = [
            "rank",
            "player",
            "team",
            "position",
            "value",
            "split",
            "year"
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
            "rank",
            "team",
            "currentSeason",
            "last3",
            "last1",
            "home",
            "away",
            "previousSeason",
            "date"
        ]

