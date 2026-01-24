# identifiers must be in string.format() form due to psycopg2 string format quirks
createUrlsTable =  '''
                        CREATE TABLE IF NOT EXISTS urls 
                        (
                            statistic varchar PRIMARY KEY,
                            url varchar
                        )
                        '''

loadUrlsTable =  '''
                INSERT INTO urls (statistic, url) 
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                '''
                       
createTeamStatTeamTable =  '''
                            CREATE TABLE IF NOT EXISTS {schema}.{tableName}
                            (
                                rank int,
                                team varchar(50), 
                                seasonDate date,
                                currentSeason decimal,
                                last3 decimal,
                                last1 decimal,
                                home decimal,
                                away decimal,
                                previousSeason decimal,

                                PRIMARY KEY (team, seasonDate)

                            )
                            '''
createTeamStatPlayerTable =  '''
                            CREATE TABLE IF NOT EXISTS {schema}.{tableName}
                            (
                                rank int,
                                player varchar(50),
                                team varchar(50),
                                position varchar(5),
                                value decimal,
                                split varchar(50),
                                year int,

                                PRIMARY KEY (player, team, split, year)
                            )
                            '''

insertTeamStats = '''
                INSERT INTO {schema}.{tableName} (rank, team, seasonDate, currentSeason, last3, last1, home, away, previousSeason)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''

insertPlayerStats = '''
                INSERT INTO {schema}.{tableName} (rank, player, team, position, value, split, year)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
    
