from Parser import Parser
import requests
import re

class Service: 

    def __init__(self):
         self.urls = self.getUrls()

    def getUrls(self):
        BASE_STATS_URL = "https://www.teamrankings.com/ncb/stats/"

        res = requests.get(BASE_STATS_URL).content.decode()

        # pattern match for links to specific ncaa basketball stats
        matches = re.finditer("/ncaa-basketball/stat/", res)
        urls = []
        for match in matches:
                index = match.span()[0]
                while res[index] != ">":
                    index += 1
                urlEnd = index - 1
                url = res[match.span()[0] : urlEnd]
                urls.append(url)
        
        return urls

    def writeUrlsToFile(self):
        with open("statsURLs.txt", "w") as f:
            for url in self.urls:
                    f.write(url +  "\n")
        f.close()

    def getTableNames(self):
        parser = Parser()
        tableNames = []
        for url in self.urls:
            tableNames.append(parser.getStatisticName(url))
        return tableNames



    
