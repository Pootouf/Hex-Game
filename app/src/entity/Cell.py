from app.src.entity import Board, Status


class Cell(object):
    board : Board
    x: int
    y: int
    status: Status

    def __init__(self, x: int, y: int, status: Status, board: Board):
        self.board = board
        self.x: int = x
        self.y: int = y
        self.status = status
        self.board = board

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getStatus(self) -> Status:
        return self.status

    def getBoard(self) -> Board:
        return self.board

    def setStatus(self, status: Status):
        self.status = status


