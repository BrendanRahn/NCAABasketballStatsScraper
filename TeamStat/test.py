from TeamStat.Service import Service
from TeamStat.Parser import Parser
from collections import defaultdict

service = Service()
parser = Parser()

ppgUrl = "https://www.teamrankings.com/ncaa-basketball/stat/points-per-game"

# pageString = service.getPageHtmlAsString(ppgUrl)


urls = service.parameterizeUrls(service.getUrls())
res = service.getOneTable()
print(res)
