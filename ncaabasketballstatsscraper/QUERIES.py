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
                            CREATE TABLE %s
                            (
                                team varchar(50) PRIMARY KEY,
                                rank int,
                                currentSeason int,
                                last3 decimal,
                                last1 decimal,
                                home decimal,
                                away decimal,
                                previousSeason decimal

                            )
                            '''


insertTeamStats = '''
                INSERT INTO %(tableName)s (team, rank, currentSeason, last3, last1, home, away, previousSeason)
                VALUES %(values)s
                '''
    
