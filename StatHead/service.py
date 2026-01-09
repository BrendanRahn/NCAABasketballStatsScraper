import requests 
from uuid import UUID, uuid4
from .sessionHelper import SessionHelper
from .parser import Parser
from .databaseHelper import DatabaseHelper
from .models.RunLog import RunLog
from datetime import datetime


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

        team = latestRunLog.team if latestRunLog else self.teams[0]
        offset = latestRunLog.row_offset if latestRunLog else 0

        for t in self.teams[self.teams.index(team):]:
            current_offset = offset if t == team else 0
            while True:
                url = self.buildUrl(t, current_offset)
                pageHtmlString = self.sessionHelper.getPageHtmlAsString(url)
                listOfGameMatchupData = self.parser.parseStatPageHtmlString(pageHtmlString)

                if not listOfGameMatchupData:
                    break #error?


                current_offset += 200 



        
        

    def init_db(self):
        teams = self.getAllTeams()
        dbHelper = DatabaseHelper()
        dbHelper.createAndLoadTeamIdTable(teams)
        dbHelper.createRunLogTable()
        



