from dataclasses import dataclass
from ncaabasketballstatsscraper import CONSTS

class Table:
    schemaName: str
    tableName: str
    columns: list
    data: list

    def __init__(self, tableName) -> None:
        self.tableName = tableName
        self.schemaName = tableName.split("_")[0]

        if self.schemaName == "player":
            self.columns = CONSTS.PLAYER_COLUMNS
        elif self.schemaName == "team":
            self.columns = CONSTS.TEAM_COLUMNS

        self.data = []

    def appendData(self, data) -> None:
        self.data += data