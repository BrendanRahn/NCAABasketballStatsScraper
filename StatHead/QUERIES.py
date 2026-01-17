# identifiers must be in string.format() form due to psycopg2 string format quirks

createStatheadScheama = '''
            CREATE SCHEMA IF NOT EXISTS stathead;
        '''

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
                status VARCHAR(50),
                timestamp TIMESTAMP WITH TIME ZONE,
                team VARCHAR(50),
                row_offset INT
                );
            '''

createGameMatchupDataTable = '''
            CREATE TABLE IF NOT EXISTS stathead.game_matchup_data (
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

getLatestRunLog = '''
                SELECT * 
                FROM stathead.run_log
                ORDER BY timestamp DESC
                LIMIT 1;
            '''

insertRunLog = '''
            INSERT INTO stathead.run_log (run_log_uuid, status, timestamp, team, row_offset)
            VALUES (%(run_log_uuid)s, %(status)s, %(timestamp)s, %(team)s, %(row_offset)s);
            '''

insertGameMatchupData = '''
            INSERT INTO stathead.game_matchup_data (team_name, date, game_location, opp_name, team_score, opp_score, result, overtime)
            VALUES (%(team_name)s, %(date)s, %(game_location)s, %(opp_name)s, %(team_score)s, %(opp_score)s, %(result)s, %(overtime)s);
            '''
