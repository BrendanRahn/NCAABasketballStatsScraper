from bs4 import BeautifulSoup
from .models.GameMatchupData import GameMatchupData
from .models.GameResult import GameResult
import re

class Parser:
    def parseTeamData(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, features="html.parser")
        teamOptions = soup.find("select", {"id": "team_id"}).find_all("option")  # type: ignore
        teamIds = [str(option["value"]) for option in teamOptions if option["value"] != ""]  # type: ignore
        return teamIds
        

    def parseStatPageHtmlString(self, html: str) -> list[GameMatchupData]:
        soup = BeautifulSoup(html, features="html.parser")
        tableBody = soup.find("tbody")  # type: ignore
        if tableBody is None:
            endOfOffsetReached = self.hasReachedEndOfOffset(soup)
            if endOfOffsetReached:
                return []
            else:
                raise Exception("Could not find table body in HTML and end of offset not reached.")

        rows = tableBody.find_all("tr")  # type: ignore

        gameMatchupDataList = []
        for row in rows:
            statsDict = {}
            for cell in row.find_all(["td"]):
                statName = cell.get("data-stat")
                statValue = cell.text.strip()
                statsDict[statName] = statValue

            gameDate = self.getDateFromTableValue(statsDict.get("date", None))
            gameLocation = self.getGameLocationFromTableValue(statsDict.get("game_location", ""))
            gameResult = self.getGameResultFromTableValue(statsDict.get("game_result", None))

            gameMatchupData = GameMatchupData(
                team_name=statsDict.get("team_name_abbr", None),
                date=gameDate,
                game_location=gameLocation,
                opp_name=statsDict.get("opp_name_abbr", None),
                team_score=gameResult.team_score,
                opp_score=gameResult.opp_score,
                result=gameResult.result,
                overtime=gameResult.overtime
            )

            gameMatchupDataList.append(gameMatchupData)

        return gameMatchupDataList
    
    def getGameLocationFromTableValue(self, tableValue: str) -> str:
        if tableValue == "@":
            return "AWAY"
        elif tableValue == "N":
            return "NEUTRAL"
        else:
            return "HOME"
        
    def getGameResultFromTableValue(self, tableValue: str) -> GameResult:
        
        #Copilot generated, surely it will work first try
        if tableValue is None:
            raise ValueError("gameResult table value cannot be None")

        if not tableValue or len(tableValue) < 5:
            raise ValueError("tableValue must be in the format 'W 100-99' or 'L 85-90'")
        result_char = tableValue[0]
        try:
            # Remove result char and space
            score_and_ot = tableValue[2:]
            # Check for overtime indicator
            overtime = 0
            if '(' in score_and_ot:
                score_part, ot_part = score_and_ot.split('(', 1)
                score_part = score_part.strip()
                ot_str = ot_part.strip().rstrip(')')
                # ot_str is like 'OT' or '2OT'
                if ot_str == 'OT':
                    overtime = 1
                elif ot_str.endswith('OT'):
                    try:
                        overtime = int(ot_str[:-2])
                    except Exception:
                        overtime = 0
            else:
                score_part = score_and_ot.strip()
            team_score_str, opp_score_str = score_part.split('-')
            team_score = int(team_score_str)
            opp_score = int(opp_score_str)
        except Exception as e:
            raise ValueError(f"Could not parse scores from tableValue '{tableValue}': {e}")
        return GameResult(
            team_score=team_score,
            opp_score=opp_score,
            result=result_char,
            overtime=overtime
        )
    
    def getDateFromTableValue(self, tableValue: str) -> str:
        if tableValue is None:
            raise ValueError("gameDate table value cannot be None")
        else:
            filteredDate = re.sub(r"[^0-9-]", "", tableValue)
            return filteredDate
            

    def hasReachedEndOfOffset(self, soup: BeautifulSoup) -> bool:
        noDataPtag = soup.find("p", string="Sorry, there are no results for your search.")
        return noDataPtag is not None