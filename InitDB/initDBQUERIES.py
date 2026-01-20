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
