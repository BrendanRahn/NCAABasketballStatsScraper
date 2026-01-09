# identifiers must be in string.format() form due to psycopg2 string format quirks

createTeamsTable = '''
            CREATE TABLE IF NOT EXISTS team_id (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                team VARCHAR(50) UNIQUE NOT NULL
            );
        '''

loadTeamId = '''
            INSERT INTO team_id (team)
            VALUES (%s)
            ON CONFLICT (team) DO NOTHING;
        '''

createRunLogTable = '''
            CREATE TABLE IF NOT EXISTS run_log (
                run_log_uuid UUID,
                status VARCHAR(50),
                timestamp TIMESTAMP WITH TIME ZONE,
                team VARCHAR(50),
                row_offset INT
                );
            '''

getLatestRunLog = '''
                SELECT * 
                FROM run_log
                ORDER BY timestamp DESC
                LIMIT 1;
            '''

insertRunLog = '''
            INSERT INTO run_log (run_log_uuid, status, timestamp, team, row_offset)
            VALUES (%(run_log_uuid)s, %(status)s, %(timestamp)s, %(team)s, %(row_offset)s);
            '''