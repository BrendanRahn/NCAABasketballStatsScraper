
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

QUERIES = {

    "checkDatabaseExists": '''
                        SELECT EXISTS
                        (
                            SELECT 1 FROM pg_catalog.pg_database 
                            WHERE datname = (%s)
                        )
                        ''',

    "createDatabase": '''
                        CREATE DATABASE (%s)
                    ''',

    "createUrlsTable": '''
                        CREATE TABLE IF NOT EXISTS urls 
                        (
                            statistic varchar PRIMARY KEY,
                            url varchar
                        )
                        ''',

    "loadUrlsTable": '''
                        INSERT INTO urls (statistic, url) 
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                     ''',
                       
    "createTeamStatTableForTeam": '''
                                    CREATE TABLE %s
                                    (
                                        team varchar(50) PRIMARY KEY,
                                        rank int,
                                        currentSeason int,
                                        last3 decimal,
                                        last1 decimal,
                                        home decimal,
                                        awaydecimal,
                                        previousSeason decimal

                                    )
                                    '''
    

}
