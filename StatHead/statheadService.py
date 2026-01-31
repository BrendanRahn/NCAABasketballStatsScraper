import requests 
from uuid import UUID, uuid4
from .sessionHelper import SessionHelper
from .statheadParser import Parser
from .statheadDBHelper import DatabaseHelper
from .models.RunLog import RunLog
from datetime import datetime
import time
import jwt
import multiprocessing


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
    
    def createNewRunLog(self, latestRunLog: RunLog, comp_type: str) -> None:
        if latestRunLog is None:
            runLog = RunLog(
            run_log_uuid=self.runUUID,
            comp_type=comp_type,
            status='START',
            timestamp=datetime.now(),
            team=self.teams[0],
            row_offset=0)

            self.dbHelper.insertRunLog(runLog)
        else:
            currentRunLog = RunLog(
                run_log_uuid=self.runUUID,
                comp_type=comp_type,
                status='START',
                timestamp=datetime.now(),
                team=latestRunLog.team,
                row_offset=latestRunLog.row_offset)
            
            self.dbHelper.insertRunLog(currentRunLog)
            
    def buildUrlRegSeason(self, team: str, offset: int) -> str:
        url = self.BASE_URL
        url += "?request=1"
        url += "&order_by=date"
        url += "&timeframe=season"
        url += "&year_min=1997"
        url += "&year_max=2026"
        url += "&comp_type=reg"
        url += "&comp_id=NCAAM"
        url += f"&team_id={team}"
        url += f"&offset={offset}"
        return url
    
    def buildUrlTournament(self, offset: int) -> str:
        url = self.BASE_URL
        url += "?request=1"
        url += "&order_by=date"
        url += "&timeframe=season"
        url += "&year_min=1997"
        url += "&year_max=2026"
        url += "&comp_type=ncaa"
        url += "&comp_id=NCAAM"
        url += "&tourn_id=ncaa"
        url += f"&offset={offset}"
        return url

    # have regularSeason in name?
    def startRun(self):
        latestRunLog = self.dbHelper.getLatestRunLogByCompType("reg")
        self.createNewRunLog(latestRunLog, comp_type="reg")

        startTeam = latestRunLog.team if latestRunLog else self.teams[0]

        startOffset = (latestRunLog.row_offset + 200) if latestRunLog else 0

        try:
            for team in self.teams[self.teams.index(startTeam):]:
                offset = startOffset if team == startTeam else 0
                while True:
                    url = self.buildUrlRegSeason(team, offset)
                    pageHtmlString = self.sessionHelper.getPageHtmlAsString(url)
                    listOfregSeasonGame = self.parser.parseRegSeasonPageHtmlString(pageHtmlString)

                    print(f"Processing reg season team {team} at offset {offset} with {len(listOfregSeasonGame)} games.")
                    if len(listOfregSeasonGame) == 0:
                        break #start next team

                    #process and store data
                    try:
                        self.dbHelper.insertRegularSeasonGames(listOfregSeasonGame)
                    except Exception as e:
                        print(f"Error inserting game matchup data for team {team} at offset {offset}: {e}")
                        errorRunLog = RunLog(
                            run_log_uuid=self.runUUID,
                            comp_type="reg",
                            status='ERROR',
                            timestamp=datetime.now(),
                            team=team,
                            row_offset=offset
                        )
                        self.dbHelper.insertRunLog(errorRunLog)
                        raise e

                    offset += 200

                    isTokenExpired = self.isSessionTokenExpired()
                    if isTokenExpired:
                        print("Session token expired. Re-authenticating...")
                        self.sessionHelper.reAuthenticateSession()
                        
                    time.sleep(7) #to avoid ip blocking, rate limit is 10 requests per second

        except KeyboardInterrupt:
            #save run log
            endRunLog = RunLog(
                run_log_uuid=self.runUUID,
                comp_type="reg",
                status='END',
                timestamp=datetime.now(),
                team=team,
                row_offset=offset
            )

            self.dbHelper.insertRunLog(endRunLog)
            print("Run interrupted by user. Progress saved.")

    def getTournamentGames(self):
        latestRunLog = self.dbHelper.getLatestRunLogByCompType("ncaa")
        self.createNewRunLog(latestRunLog, comp_type="ncaa")

        startOffset = (latestRunLog.row_offset + 200) if latestRunLog else 0

        try:
            endOfDataRecahed = False
            offset = startOffset
            while not endOfDataRecahed:
                url = self.buildUrlTournament(offset)
                pageHtmlString = self.sessionHelper.getPageHtmlAsString(url)

                listOfTournamentGames = self.parser.parseTournamentPageHtmlString(pageHtmlString)

                print(f"Processing tournament at offset {offset} with {len(listOfTournamentGames)} games.")
                if len(listOfTournamentGames) == 0:
                    endOfDataRecahed = True
                    break

                #process and store data
                try:
                    self.dbHelper.insertTournamentGames(listOfTournamentGames)
                except Exception as e:
                    print(f"Error inserting tournament game data at offset {offset}: {e}")
                    errorRunLog = RunLog(
                        run_log_uuid=self.runUUID,
                        comp_type="ncaa",
                        status='ERROR',
                        timestamp=datetime.now(),
                        team=None,
                        row_offset=offset
                    )
                    self.dbHelper.insertRunLog(errorRunLog)
                    raise e

                offset += 200

                isTokenExpired = self.isSessionTokenExpired()
                if isTokenExpired:
                    print("Session token expired. Re-authenticating...")
                    self.sessionHelper.reAuthenticateSession()
                        
                time.sleep(7) #to avoid ip blocking, rate limit is 10 requests per second
        except KeyboardInterrupt:
            #save run log
            endRunLog = RunLog(
                run_log_uuid=self.runUUID,
                comp_type="ncaa",
                status='END',
                timestamp=datetime.now(),
                team=None,
                row_offset=offset
            )

            self.dbHelper.insertRunLog(endRunLog)
            print("Run interrupted by user. Progress saved.")


    # TODO: change this to check if token is near expiry rather than fully expired
    def isSessionTokenExpired(self) -> bool:
        token = self.sessionHelper.SESSION.cookies.get("access_token")
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decoded_token.get("exp")
        current_timestamp = int(time.time())
        return exp_timestamp < current_timestamp

    def init_db(self):
        teams = self.getAllTeams()
        dbHelper = DatabaseHelper()
        dbHelper.createAndLoadTeamIdTable(teams)
        dbHelper.createRunLogTable()
        dbHelper.createRegularSeasonGamesTable()
        dbHelper.createTournamentGamesTable()

# Top-level function for multiprocessing
def run_stathead_service(queue: multiprocessing.Queue):
    svc = Service()
    try: 
        # svc.startRun()
        svc.getTournamentGames()
    except Exception as e:
        queue.put(f"An error occurred in StatHead service: {e}")
        queue.put(f"sessionTokenExpired? : {svc.isSessionTokenExpired()}")
        



