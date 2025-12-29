import dotenv
import psycopg2
import os
from . import QUERIES

class DatabaseHelper:

    def __init__(self):
        self.connection = self.getDatabaseConnection()

    # __del__ function to close db connection?

    def getDatabaseConnection(self) -> psycopg2.extensions.connection:
        dotenv.load_dotenv()

        conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("STATHEAD_TEST_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
        conn = psycopg2.connect(conn_string)

        return conn

    #TODO: thinking about initalizing entire db at root level, and onyl handling inserts at sublevels
    def createAndLoadTeamIdTable(self, teamIds: list[str]):
        cursor = self.connection.cursor()
        tableData = [(teamId,) for teamId in teamIds]

        cursor.execute(query=QUERIES.createTeamsTable)
        cursor.executemany(
            query=QUERIES.loadTeamId,
            vars_list=tableData
        )
        self.connection.commit()
        cursor.close()

    def createRunLogTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=QUERIES.createRunLogTable)
        self.connection.commit()
        cursor.close()

    def getLatestRunLog(self):
        cursor = self.connection.cursor()
        cursor.execute(query=QUERIES.getLatestRunLog)
        result = cursor.fetchone()
        cursor.close()
        return result


