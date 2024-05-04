from src.entity import Board, Status


class Cell(object):
    x: int
    y: int
    status: Status

    def __init__(self, x: int, y: int, status: Status):
        self.x: int = x
        self.y: int = y
        self.status = status

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getStatus(self) -> Status:
        return self.status

    def setStatus(self, status: Status):
        self.status = status

    def copy(self):
        return Cell(self.x, self.y, self.status)
