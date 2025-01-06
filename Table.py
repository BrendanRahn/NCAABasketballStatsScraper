from dataclasses import dataclass

class Table:
    tableName: str
    columns: list
    data: list = []


    def appendData(self, data) -> None:
        self.data += data