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
        
    class DataParser:
        # def __init__(self, string):
        #     self.index = len(string) - 1
        #     self.string = string

        # def __iter__(self):
        #     return self
        
        # def __next__(self):
        #     if (self.index >= len(self.string)):
        #         raise StopIteration
        #     x = self.string[self.index]
        #     self.index -= 1
        #     return x

        def getColumnNames(self, string):
            soup = BeautifulSoup(string)
            theaders = soup.thead.find_all("th")
            return [th.string for th in theaders]

        def getData(self, string):
            soup = BeautifulSoup(string)
            tbody = soup.tbody.find_all("tr")
            test = tbody[0].find_all("td")
            data = []  
            for tr in tbody:
                values = [td.string for td in tr.find_all("td")]
                data.append(values)
            return data


    def getStatisticName(self, url: str) -> str:
        urlAsIter = iter(self.ReverseIterator(url))

        statisticName = ""
        for chr in urlAsIter:
            match chr:
                case "-":
                    statisticName = "_" + statisticName
                case "/":
                    return statisticName
                case _:
                    statisticName = chr + statisticName


    # def getStatisticData(self, string):
    #     data = {}
    #     for chr in string:
    #         match chr:


