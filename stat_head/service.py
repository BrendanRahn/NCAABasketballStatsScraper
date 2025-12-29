import requests 
from .sessionHelper import SessionHelper
from .parser import Parser
from .databaseHelper import DatabaseHelper


class Service:
    def __init__(self):
        self.sessionHelper = SessionHelper()
        self.parser = Parser()
        self.teamIds = self.getAllTeams()

    def getAllTeams(self) -> list[str]:
        pageHtml = self.sessionHelper.getAllTeams()
        listOfTeams = self.parser.parseTeamData(pageHtml)
        return listOfTeams
    
    # def createRunStartLog(self):


    def init_db(self):
        teams = self.getAllTeams()
        dbHelper = DatabaseHelper()
        dbHelper.createAndLoadTeamIdTable(teams)
        dbHelper.createRunLogTable()
        



