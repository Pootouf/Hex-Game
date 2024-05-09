from typing import Self

from src.entity import Board, Status


class Cell(object):
    x: int
    y: int
    status: Status
    neighbours: list

    def __init__(self, x: int, y: int, status: Status):
        self.x: int = x
        self.y: int = y
        self.status = status
        self.neighbours = list()

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getStatus(self) -> Status:
        return self.status

    def getNeighbours(self) -> list:
        return self.neighbours

    def setStatus(self, status: Status):
        self.status = status

    def addNeighbour(self, neighbour : Self) -> None:
        self.neighbours.append(neighbour)

    def copy(self):
        return Cell(self.x, self.y, self.status)
