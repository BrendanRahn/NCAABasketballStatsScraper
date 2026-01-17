import dotenv
import psycopg
from psycopg.rows import class_row
import os
from . import QUERIES
from .models.RunLog import RunLog
from .models.GameMatchupData import GameMatchupData

class DatabaseHelper:

    def __init__(self):
        self.connection = self.getDatabaseConnection()

    # __del__ function to close db connection?

    def getDatabaseConnection(self) -> psycopg.Connection:
        dotenv.load_dotenv()

        conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("STATHEAD_TEST_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
        conn = psycopg.connect(conn_string)
        return conn

    #TODO: thinking about initalizing entire db at root level, and onyl handling inserts at sublevels
    def createAndLoadTeamIdTable(self, teamIds: list[str]):
        cursor = self.connection.cursor()
        tableData = [(teamId,) for teamId in teamIds]

        cursor.execute(query=QUERIES.createTeamsTable)
        cursor.executemany(
            query=QUERIES.loadTeamId,
            params_seq=tableData
        )
        self.connection.commit()
        cursor.close()

    def createRunLogTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=QUERIES.createRunLogTable)
        self.connection.commit()
        cursor.close()

    def createGameMatchupDataTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=QUERIES.createGameMatchupDataTable)
        self.connection.commit()
        cursor.close()

    def getLatestRunLog(self):
        cursor = self.connection.cursor(row_factory=class_row(RunLog))
        cursor.execute(query=QUERIES.getLatestRunLog)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def insertRunLog(self, runLog: RunLog):
        cursor = self.connection.cursor()
        cursor.execute(
            query=QUERIES.insertRunLog,
            params=runLog.model_dump()
        )
        self.connection.commit()
        cursor.close()

    #TODO: create test case to validate all 200 rows inserted correctly
    def insertGameMatchupData(self, gameMatchupData: list[GameMatchupData]):
        cursor = self.connection.cursor()
        cursor.executemany(
            query=QUERIES.insertGameMatchupData,
            params_seq=[game.model_dump() for game in gameMatchupData]
        )
        self.connection.commit()
        cursor.close()


