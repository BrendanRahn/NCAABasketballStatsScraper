from .Parser import Parser
from .Table import Table
from . import CONSTS
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import time
import re

class Service: 
    parser = Parser()

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
        tags = soup.main.find_all("a") # type: ignore
        routes = [tag["href"] for tag in tags if len(tag["href"]) > 1] # type: ignore
        urls = [BASE_URL + route for route in routes] # type: ignore
        
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
        
        tableNames = []
        for url in self.URLS:
            tableNames.append(self.parser.getTableName(url))
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
        #rename - sorted how?
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
    
    def getTablesAndTheirUrls(self) -> dict:
        urlsByTable = defaultdict(list)
        parameterizedUrls = self.getParameterizeUrls(self.URLS)
        for url in parameterizedUrls:
            tableName = self.parser.getTableName(url)
            urlsByTable[tableName].append(url)

        return urlsByTable

    
    def getDataForTable(self, tableName: str, tableUrls: list[str]) -> Table:

        table = Table(tableName)

        for url in tableUrls:
            paramsAndValues = self.parser.getParamsAndValuesDict(url)
            if len(paramsAndValues) > 1:
                #make new entry for year, from season_id
                paramsAndValues["year"] = CONSTS.SEASON_IDS_TO_YEARS[paramsAndValues["season_id"]]

            # sleep for 1s to avoid (potentially?) getting ip blocked
            print(f'getting data for {table.tableName} + {paramsAndValues["year"]}')
            time.sleep(1)
            html = self.getPageHtmlAsString(url)
            
            data = [row.append(paramsAndValues["year"]) for row in self.parser.getData(html)]
            table.appendData(data)


        return table
            
    #temporary
    def getOneTable(self, tableName: str, tableUrls: list[str]) -> Table:
        firstUrl = tableUrls[0]

        table = Table(tableName)

        if table.schemaName == "player":
            table.columns = CONSTS.PLAYER_COLUMNS
        elif table.schemaName == "team":
            table.columns = CONSTS.TEAM_COLUMNS

        for url in tableUrls:
            paramsAndValues = self.parser.getParamsAndValuesDict(url)
            if len(paramsAndValues) > 1:
                #make new entry for year, from season_id
                paramsAndValues["year"] = CONSTS.SEASON_IDS_TO_YEARS[paramsAndValues["season_id"]]
                
            # sleep for 1s to avoid (potentially?) getting ip blocked
            print(f'getting data for {table.tableName} + {paramValues}')
            time.sleep(1)
            html = self.getPageHtmlAsString(url)
            
            data = [row + paramValues for row in self.parser.getData(html)]
            table.appendData(data)

        
        return table
    
    #temporary
    def getOneUrlDataForTable(self, tableName: str, tableUrls: list[str]) -> Table:
        firstUrl = tableUrls[0]

        table = Table(tableName)
        table.schemaName = self.parser.getSchemaName(firstUrl)
        table.tableName = tableName

        if table.schemaName == "player":
            table.columns = CONSTS.PLAYER_COLUMNS
            return Table("empty") #todo: remove this line, temporary fix for player table not being created
        elif table.schemaName == "team":
            table.columns = CONSTS.TEAM_COLUMNS


        paramsAndValues = self.parser.getParamsAndValuesDict(tableUrls[0])
        if len(paramsAndValues) > 1:
            #make new entry for year, from season_id

            #TODO: player stats have user_id, team stats have year date
            paramsAndValues["year"] = CONSTS.SEASON_IDS_TO_YEARS[paramsAndValues["season_id"]]
            
        # sleep for 1s to avoid (potentially?) getting ip blocked
        print(f'getting data for {table.tableName} + {paramsAndValues["year"]}')
        time.sleep(1)
        html = self.getPageHtmlAsString(tableUrls[0])
        
        listData = self.parser.getData(html)

        if table.schemaName == "player":
            # listData[valueColumnIndex] = parser.sanitizeNumericData(listData[valueColumnIndex])
            
            listData = self.processPlayerData(listData, paramsAndValues)
        elif table.schemaName == "team":
            # need to add year (example) to data row
            listData = self.processTeamData(listData, paramsAndValues)

        table.appendData(listData)      
        return table
    

    def processPlayerData(self, data: list[list[str]], urlParamValues: dict[str, str]) -> list[list[str]]:
        sanitizedData = [self.parser.sanitizeData(row) for row in data]
        dataWithYear = [row + [urlParamValues["year"]] for row in sanitizedData]
        return dataWithYear
    
    def processTeamData(self, data: list[list[str]], urlParamValues: dict[str, str]) -> list[str]:
        sanitizedData = [self.parser.sanitizeData(row) for row in data]
        currentSeason

        dataWithCurrentSeason = [row[:1] + [urlParamValues["year"]] + row[1:] for row in sanitizedData]
        dataWithPreviousS
        return dataWithCurrentSeason
    





