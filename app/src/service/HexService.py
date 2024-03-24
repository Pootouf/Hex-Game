from src.entity.Board import Board
from src.entity.Bot import Bot
from src.entity.Cell import Cell
from src.entity.HexGame import HexGame
from src.entity.Player import Player
from src.entity.Status import Status


def createGame(boardSize: int, difficultyLevel: int) -> HexGame:

    cells = []
    for i in range(boardSize):
        cellList = []
        for j in range(boardSize):
            cellList.append(Cell(i, j, Status.NONE))
        cells.append(cellList)
    board = Board(cells)

    player = Player("blue")
    bot = Bot("red")

    return HexGame(difficultyLevel, player, board, bot)

