import re
from bs4 import BeautifulSoup
class Parser:

    class ReverseIterator:
        def __init__(self, string):
            self.index = len(string) - 1
            self.string = string

        def __iter__(self):
            return self
        def __next__(self):
            if (self.index < 0):
                raise StopIteration
            x = self.string[self.index]
            self.index -= 1
            return x
        

    def getData(self, string: str):
        soup = BeautifulSoup(string, features="html.parser")
        trows = soup.tbody.find_all("tr")
        data = []  
        for tr in trows:
            rowData = [td.string for td in tr.find_all("td")]
            data.append(rowData)
        return data
    
    # def sanitizeData(self, row: list) -> list:
        # try:
        #     map(lambda x: int(x), row)
        # except:
            


    def getTableName(self, url: str) -> str:
        try: 
            url = url[:url.index("?")]
        except:
            url = url
        urlAsRIter = iter(self.ReverseIterator(url))

        tableName = ""
        #TODO: change table names to camelCase? redo function with recursion and pass capitalizeNextLetter toggle
        for chr in urlAsRIter:
            match chr:
                case "-":
                    tableName = "_" + tableName
                case "/":
                    break
                case _:
                    tableName = chr + tableName

        if re.search("player-stat", url):
            tableName = "player_" + tableName
        else:
            tableName = "team_" + tableName
        
        return tableName


    def getParamValues(self, url: str) -> list[str]:
        return re.findall("(?<=\=)([^&]*)(?=\&)", url)
        


