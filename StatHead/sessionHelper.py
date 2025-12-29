import requests
import dotenv
import os

class SessionHelper:

    def __init__(self):
        self.SESSION = self.loginAndGetSession()

    def loginAndGetSession(self) -> requests.Session:
        dotenv.load_dotenv()

        session = requests.Session()
        login_url = "https://www.sports-reference.com/users/login.cgi"

        payload = {
            "username": os.getenv("STATHEAD_USERNAME"),
            "password": os.getenv("STATHEAD_PASSWORD")
        }
        session.post(login_url, data=payload,)

        if session.cookies.get("access_token") is None:
            raise Exception("Login failed")
        else:
            return session
        
    def getAllTeams(self) -> list[str]:
        teams_url = "https://www.sports-reference.com/stathead/basketball/cbb/team-game-finder.cgi"
        res = self.SESSION.get(teams_url).content.decode()
        return res