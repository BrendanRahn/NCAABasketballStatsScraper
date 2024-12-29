from Parser import Parser
from bs4 import BeautifulSoup
import requests
import re

class Service: 

    def __init__(self):
         self.urls = self.getUrls()

    def getUrls(self) -> list[str]:
        BASE_STATS_URL = "https://www.teamrankings.com/ncb/stats/"

        res = requests.get(BASE_STATS_URL).content.decode()
        soup = BeautifulSoup(res)
        tags = soup.main.find_all("a")
        urls = [tag["href"] for tag in tags if len(tag["href"]) > 1]
        
        return urls
    
    def getPageData(self, url: str) -> str:
         res = requests.get(url).content.decode()
         return res
         

    def writeUrlsToFile(self) -> None:
        with open("statsURLs.txt", "w") as f:
            for url in self.urls:
                    f.write(url +  "\n")
        f.close()

    def getTableNames(self) -> list[str]:
        parser = Parser()
        tableNames = []
        for url in self.urls:
            tableNames.append(parser.getStatisticName(url))
        return tableNames




