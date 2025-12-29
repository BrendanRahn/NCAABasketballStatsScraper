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
                run_log_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                start_time TIMESTAMP WITH TIME ZONE,
                end_time TIMESTAMP WITH TIME ZONE,
                start_team VARCHAR(50),
                start_offset INT,
                end_team VARCHAR(50),
                end_offset INT
                );
            '''

getLatestRunLog = '''
                SELECT * 
                FROM run_log
                ORDER BY run_log_id DESC
                LIMIT 1;
            '''