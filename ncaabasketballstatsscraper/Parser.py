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
        

    def getData(self, string: str) -> list[list[str]]:
        soup = BeautifulSoup(string, features="html.parser")
        trows = soup.tbody.find_all("tr") # type: ignore
        data = []
        for tr in trows:
            rowData = (tr.find_all("td"))  # type: ignore
            stringData = [d.get_text().strip() for d in rowData]
            data.append(stringData)
        return data
    
            
    def sanitizeData(self, data: list[str]) -> list[str]:
        return [re.sub(r'%', '', d) for d in data] # type: ignore


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
    
    def getSchemaName(self, url: str) -> str:
        if re.search("player-stat", url):
            schemaName = "player"
        else:
            schemaName = "team"

        return schemaName   

    #reanme getUrlParams?
    def getParamsAndValuesDict(self, url: str) -> dict[str, str]:
        listOfParamsAndValues = re.findall("(?<=[?&])([^=&#]+)=([^&#]*)", url)
        paramsAndValues = {param: value for param, value in listOfParamsAndValues}
        return paramsAndValues
        


