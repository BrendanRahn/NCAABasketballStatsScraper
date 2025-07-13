# identifiers must be in string.format() form due to psycopg2 string format quirks
checkDatabaseExists = '''
                        SELECT EXISTS
                        (
                            SELECT 1 FROM pg_catalog.pg_database 
                            WHERE datname = '{database}'
                        )
                        '''

createDatabase = '''
                CREATE DATABASE {database}
                '''

createSchema =  '''
                CREATE SCHEMA IF NOT EXISTS {schema}
                '''

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
                            CREATE TABLE IF NOT EXISTS {tableName}
                            (
                                rank int,
                                team varchar(50), 
                                currentSeason int,
                                last3 decimal,
                                last1 decimal,
                                home decimal,
                                away decimal,
                                previousSeason decimal,

                                PRIMARY KEY (team, currentSeason)

                            )
                            '''
createTeamStatPlayerTable =  '''
                            CREATE TABLE IF NOT EXISTS {tableName}
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
                INSERT INTO {tableName} (team, rank, currentSeason, last3, last1, home, away, previousSeason)
                VALUES %s
                '''

insertPlayerStats = '''
                INSERT INTO {tableName} (rank, player, team, position, value, split, year)
                VALUES %s
                '''
    
