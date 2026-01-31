# identifiers must be in string.format() form due to psycopg2 string format quirks

createTeamsTable = '''
            CREATE TABLE IF NOT EXISTS stathead.team_id (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                team VARCHAR(50) UNIQUE NOT NULL
            );
        '''

loadTeamId = '''
            INSERT INTO stathead.team_id (team)
            VALUES (%s)
            ON CONFLICT (team) DO NOTHING;
        '''

createRunLogTable = '''
            CREATE TABLE IF NOT EXISTS stathead.run_log (
                run_log_uuid UUID,
                comp_type VARCHAR(20),
                status VARCHAR(50),
                timestamp TIMESTAMP WITH TIME ZONE,
                team VARCHAR(50),
                row_offset INT
                );
            '''

getLatestRunLogByCompType = '''
                SELECT * 
                FROM stathead.run_log
                WHERE comp_type = %(comp_type)s
                ORDER BY timestamp DESC
                LIMIT 1;
            '''

insertRunLog = '''
            INSERT INTO stathead.run_log (run_log_uuid, comp_type, status, timestamp, team, row_offset)
            VALUES (%(run_log_uuid)s, %(comp_type)s, %(status)s, %(timestamp)s, %(team)s, %(row_offset)s);
            '''

createRegularSeasonGamesTable = '''
            CREATE TABLE IF NOT EXISTS stathead.regular_season_games (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                team_name VARCHAR(50),
                date DATE,
                game_location VARCHAR(10),
                opp_name VARCHAR(50),
                team_score INT,
                opp_score INT,
                result VARCHAR(5),
                overtime INT
            );
        '''

insertRegularSeasonGame = '''
            INSERT INTO stathead.regular_season_games (team_name, date, game_location, opp_name, team_score, opp_score, result, overtime)
            VALUES (%(team_name)s, %(date)s, %(game_location)s, %(opp_name)s, %(team_score)s, %(opp_score)s, %(result)s, %(overtime)s);
        '''
createTournamentGamesTable = '''
            CREATE TABLE IF NOT EXISTS stathead.tournament_games (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                team_name VARCHAR(50),
                date DATE,
                game_location VARCHAR(10),
                opp_name VARCHAR(50),
                team_score INT,
                opp_score INT,
                result VARCHAR(5),
                overtime INT
            );
        '''
insertTournamentGame = '''
            INSERT INTO stathead.tournament_games (team_name, date, game_location, opp_name, team_score, opp_score, result, overtime)
            VALUES (%(team_name)s, %(date)s, %(game_location)s, %(opp_name)s, %(team_score)s, %(opp_score)s, %(result)s, %(overtime)s);
        '''