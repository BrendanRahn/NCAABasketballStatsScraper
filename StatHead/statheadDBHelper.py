import dotenv
import psycopg
from psycopg.rows import class_row
import os
from . import statheadQUERIES
from .models.RunLog import RunLog
from .models.RegSeasonGame import RegSeasonGame
from models.TournamentGame import TournamentGame

class DatabaseHelper:

    def __init__(self):
        self.connection = self.getDatabaseConnection()

    # __del__ function to close db connection?


    def getDatabaseConnection(self) -> psycopg.Connection:
        dotenv.load_dotenv()

        conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
        conn = psycopg.connect(conn_string)
        return conn

    def createAndLoadTeamIdTable(self, teamIds: list[str]):
        cursor = self.connection.cursor()
        tableData = [(teamId,) for teamId in teamIds]

        cursor.execute(query=statheadQUERIES.createTeamsTable)
        cursor.executemany(
            query=statheadQUERIES.loadTeamId,
            params_seq=tableData
        )
        self.connection.commit()
        cursor.close()

    def createRunLogTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=statheadQUERIES.createRunLogTable)
        self.connection.commit()
        cursor.close()

    def createRegularSeasonGamesTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=statheadQUERIES.createRegularSeasonGamesTable)
        self.connection.commit()
        cursor.close()

    def createTournamentGamesTable(self):
        cursor = self.connection.cursor()
        cursor.execute(query=statheadQUERIES.createTournamentGamesTable)
        self.connection.commit()
        cursor.close()

    def getLatestRunLogByCompType(self, comp_type: str):
        cursor = self.connection.cursor(row_factory=class_row(RunLog))
        cursor.execute(query=statheadQUERIES.getLatestRunLogByCompType, 
                       params={"comp_type": comp_type})
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def insertRunLog(self, runLog: RunLog):
        cursor = self.connection.cursor()
        cursor.execute(
            query=statheadQUERIES.insertRunLog,
            params=runLog.model_dump()
        )
        self.connection.commit()
        cursor.close()

    #TODO: create test case to validate all 200 rows inserted correctly
    def insertRegularSeasonGames(self, games: list[RegSeasonGame]):
        cursor = self.connection.cursor()
        cursor.executemany(
            query=statheadQUERIES.insertRegularSeasonGame,
            params_seq=[game.model_dump() for game in games]
        )
        self.connection.commit()
        cursor.close()

    def insertTournamentGames(self, games: list[TournamentGame]):
        cursor = self.connection.cursor()
        cursor.executemany(
            query=statheadQUERIES.insertTournamentGame,
            params_seq=[game.model_dump() for game in games]
        )
        self.connection.commit()
        cursor.close()


