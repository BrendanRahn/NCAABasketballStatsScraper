from bs4 import BeautifulSoup

class Parser:
    def parseTeamData(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, features="html.parser")
        teamOptions = soup.find("select", {"id": "team_id"}).find_all("option")  # type: ignore
        teamIds = [str(option["value"]) for option in teamOptions if option["value"] != ""]  # type: ignore
        return teamIds
        
    