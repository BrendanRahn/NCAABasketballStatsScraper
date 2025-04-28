from .Parser import Parser
from .Table import Table
from . import CONSTS
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import time
import re

class Service: 

    def __init__(self):
         self.URLS = self.getUrls()
         self.DATES = self.generateDates()
         self.SPLITS = CONSTS.PLAYER_SPLITS

    def generateDates(self) -> list[str]:
         years = map(lambda x : str(x), range(1997, 2024, 1))
         dates = [
              "01-01", #midseason
              "03-01" #endseason
         ]
         return [year + "-" + date for year in years for date in dates]

    def getUrls(self) -> list[str]:
        BASE_URL = "https://www.teamrankings.com"
        STATS_URL = "https://www.teamrankings.com/ncb/stats/"

        res = requests.get(STATS_URL).content.decode()
        soup = BeautifulSoup(res, features="html.parser")
        tags = soup.main.find_all("a")
        routes = [tag["href"] for tag in tags if len(tag["href"]) > 1]
        urls = [BASE_URL + route for route in routes]
        
        return urls
    
    def getPageHtmlAsString(self, url: str) -> str:
         res = requests.get(url).content.decode()
         return res
         
    def writeUrlsToFile(self) -> None:
        with open("statsURLs.txt", "w") as f:
            for url in self.URLS:
                    f.write(url +  "\n")
        f.close()

    # Obsolete?
    def getTableNames(self) -> list[str]:
        parser = Parser()
        tableNames = []
        for url in self.URLS:
            tableNames.append(parser.getTableName(url))
        return tableNames
    
    def addSplitsToPlayerUrls(self, urls, splits):
        return [url + "?split=" + split + "&season_id=" + seasonId + "&"
                for url in urls
                for split in splits
                for seasonId in CONSTS.SEASON_IDS_TO_YEARS.keys()]
    
    def addDatesToTeamUrls(self, urls, dates):
         return [url + "?date=" + date + "&"
                for url in urls 
                for date in dates]
    
    
    def getParameterizeUrls(self, urls) -> list[str]:
        sortedUrls = {
              "player-stat": [],
              "team-stat": []
        }
        for url in urls:
            if re.search("player-stat", url):
                sortedUrls["player-stat"].append(url)
            else:
                sortedUrls["team-stat"].append(url)

        return (
                self.addSplitsToPlayerUrls(sortedUrls["player-stat"], self.SPLITS)
                +
                self.addDatesToTeamUrls(sortedUrls["team-stat"], self.DATES)
                )
    
    def getSortedUrlsByTable(self) -> dict:
        parser = Parser()
        urlsByTable = defaultdict(list)
        parameterizedUrls = self.getParameterizeUrls(self.URLS)
        for url in parameterizedUrls:
            tableName = parser.getTableName(url)
            urlsByTable[tableName].append(url)

        return urlsByTable

    
    def getDataForTable(self, tableName: str, tableUrls: list[str]) -> list[Table]:
        parser = Parser()

        table = Table()
        table.tableName = tableName
        table.columns = CONSTS.TEAM_COLUMNS 

        for url in tableUrls:
            paramValues = parser.getParamValues(url)
            if len(paramValues) > 1:
                paramValues[-1] = CONSTS.SEASON_IDS_TO_YEARS[paramValues[-1]]

            # sleep for 1s to avoid (potentially?) getting ip blocked
            print(f'getting data for {table.tableName} + {paramValues}')
            time.sleep(1)
            html = self.getPageHtmlAsString(url)
            
            data = [row + paramValues for row in parser.getData(html)]
            table.appendData(data)


        return table
            
    #temporary
    def getOneTable(self) -> list[Table]:
        parser = Parser()
        urlsWithParam = self.parameterizeUrls(self.URLS)
        sortedUrlsByTable = self.sortUrlsByTable(urlsWithParam)

        tables = []
        tableName = next(iter(sortedUrlsByTable))
        table = Table()
        table.tableName = tableName
        table.columns = CONSTS.TEAM_COLUMNS 

        for url in sortedUrlsByTable[tableName]:
            paramValues = parser.getParamValues(url)
            if len(paramValues) > 1:
                paramValues[-1] = CONSTS.SEASON_IDS_TO_YEARS[paramValues[-1]]
                
            # sleep for 1s to avoid (potentially?) getting ip blocked
            print(f'getting data for {table.tableName} + {paramValues}')
            time.sleep(1)
            html = self.getPageHtmlAsString(url)
            
            data = [row + paramValues for row in parser.getData(html)]
            table.appendData(data)

        tables.append(table)
        return tables


    





