from src.entity.Board import Board
from src.entity.HexGame import HexGame
from src.entity.Status import Status


"""
    getWinner: return the value of the winner of the game
    :param game, the current game of Hex:
    :return the winner of the game:
"""
def getWinner(board: Board) -> Status:
    # Evaluate if the game is ended by the player
    startColumn = __getColumnOfMatrix(0, board)
    startColumn = list(filter(lambda cell: cell.getStatus() == Status.PLAYER, startColumn))
    endColumn = __getColumnOfMatrix(board.getSideLength() - 1, board)
    hasGameEndedByPlayer = __hasGameEnded(startColumn, endColumn, Status.PLAYER)

    winner = Status.NONE
    if hasGameEndedByPlayer:
        winner = Status.PLAYER

    # Evaluate if the game is ended by the bot
    startLine = board.getCells()[0].copy()
    startLine = list(filter(lambda cell: cell.getStatus() == Status.BOT, startLine))
    endLine = board.getCells()[board.getSideLength() - 1].copy()
    hasGameEndedByBot = __hasGameEnded(startLine, endLine, Status.BOT)

    if hasGameEndedByBot:
        winner = Status.BOT

    return winner


"""
   getColumnOfMatrix : return the wanted column of i index with first value of each row
   :param i, the index of the column:
   :param board, the board in which the column must be taken: 
   :return the column with first value of each row: 
"""
def __getColumnOfMatrix(i: int, board: Board) -> list:
    if 0 > i or i > len(board.getCells()):
        raise ValueError

    column = list()
    for row in board.getCells():
        column.append(row[i])

    return column


"""
   hasGameEnded : return if the game is over
   :param i, the index of the column:
   :return the column with first value of each row: 
"""
def __hasGameEnded(cellsToTreat: list, goalCells: list, player: Status) -> bool:
    treatedCells = list()
    while cellsToTreat:
        cell = cellsToTreat.pop()
        if cell in goalCells:
            return True
        neighbours = cell.getNeighbours()
        for neighbour in neighbours:
            if (neighbour.getStatus() == player and not (neighbour in treatedCells)
                    and not (neighbour in cellsToTreat)):
                cellsToTreat.append(neighbour)
        treatedCells.append(cell)
    return False