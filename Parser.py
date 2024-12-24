class Parser:

    class UrlParser:
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

    def getStatisticName(self, url):
        parser = self.UrlParser(url)
        urlString = iter(parser)

        statisticName = ""
        for chr in urlString:
            match chr:
                case "-":
                    statisticName = "_" + statisticName
                case "/":
                    return statisticName
                case _:
                    statisticName = chr + statisticName

