from src.entity import Cell


class Board(object):
    cells: list[list[Cell]]

    def __init__(self, cells):
        self.cells = cells

    def getCell(self, x, y) -> Cell:
        return self.cells[x][y]

    def getCells(self) -> list[list[Cell]]:
        return self.cells

    def getSideLength(self) -> int:
        return len(self.cells)
