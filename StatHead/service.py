import requests 
from uuid import UUID, uuid4
from .sessionHelper import SessionHelper
from .parser import Parser
from .databaseHelper import DatabaseHelper
from .models.RunLog import RunLog
from datetime import datetime
import time


class Service:
    def __init__(self):
        self.sessionHelper = SessionHelper()
        self.dbHelper = DatabaseHelper()
        self.parser = Parser()
        self.teams = self.getAllTeams()
        self.runUUID = uuid4()
        self.BASE_URL = "https://www.sports-reference.com/stathead/basketball/cbb/team-game-finder.cgi"

    def getAllTeams(self) -> list[str]:
        pageHtml = self.sessionHelper.getAllTeams()
        listOfTeams = self.parser.parseTeamData(pageHtml)
        return listOfTeams
    
    def createNewRunLog(self, latestRunLog: RunLog) -> None:
        if latestRunLog is None:
            runLog = RunLog(
            run_log_uuid=self.runUUID,
            status='START',
            timestamp=datetime.now(),
            team=self.teams[0],
            row_offset=0)

            self.dbHelper.insertRunLog(runLog)
        else:
            currentRunLog = RunLog(
                run_log_uuid=self.runUUID,
                status='START',
                timestamp=datetime.now(),
                team=latestRunLog.team,
                row_offset=latestRunLog.row_offset)
            
            self.dbHelper.insertRunLog(currentRunLog)
            
    def buildUrl(self, team: str, offset: int) -> str:
        url = self.BASE_URL
        url += "?request=1"
        url += "&order_by=date"
        url += "&timeframe=season"
        url += "&year_min=1997"
        url += "&year_max=2026"
        url += "&comp_type=any"
        url += "&comp_id=NCAAM"
        url += f"&team_id={team}"
        url += f"&offset={offset}"
        return url

    def startRun(self):

        latestRunLog = self.dbHelper.getLatestRunLog()
        self.createNewRunLog(latestRunLog)

        startTeam = latestRunLog.team if latestRunLog else self.teams[0]

        startOffset = (latestRunLog.row_offset + 200) if latestRunLog else 0

        try:
            for team in self.teams[self.teams.index(startTeam):]:
                offset = startOffset if team == startTeam else 0
                while True:
                    url = self.buildUrl(team, offset)
                    pageHtmlString = self.sessionHelper.getPageHtmlAsString(url)
                    listOfGameMatchupData = self.parser.parseStatPageHtmlString(pageHtmlString)

                    print(f"Processing team {team} at offset {offset} with {len(listOfGameMatchupData)} games.")
                    if len(listOfGameMatchupData) == 0:
                        break #start next team

                    #process and store data
                    try:
                        self.dbHelper.insertGameMatchupData(listOfGameMatchupData)
                    except Exception as e:
                        print(f"Error inserting game matchup data for team {team} at offset {offset}: {e}")
                        errorRunLog = RunLog(
                            run_log_uuid=self.runUUID,
                            status='ERROR',
                            timestamp=datetime.now(),
                            team=team,
                            row_offset=offset
                        )
                        self.dbHelper.insertRunLog(errorRunLog)
                        raise e

                    offset += 200
                    time.sleep(7) #to avoid ip blocking, rate limit is 10 requests per second
        except KeyboardInterrupt:
            #save run log
            endRunLog = RunLog(
                run_log_uuid=self.runUUID,
                status='END',
                timestamp=datetime.now(),
                team=team,
                row_offset=offset
            )

            self.dbHelper.insertRunLog(endRunLog)
            print("Run interrupted by user. Progress saved.")

        
        

    def init_db(self):
        teams = self.getAllTeams()
        dbHelper = DatabaseHelper()
        dbHelper.createAndLoadTeamIdTable(teams)
        dbHelper.createRunLogTable()
        dbHelper.createGameMatchupDataTable()
        



