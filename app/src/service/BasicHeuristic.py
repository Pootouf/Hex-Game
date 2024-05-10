from src.entity.Board import Board
from src.entity.Status import Status


def calculateHeuristicValueForBoard(board: Board) -> int:
    cells = board.getCells()

    botValue = 0
    playerValue = 0
    previousBranch = {}
    for i in range(board.getSideLength()):
        currentBranch = {}
        for j in range(board.getSideLength()):
            cellBot = cells[i][j]
            cellPlayer = cells[j][i]
            if cellBot.getStatus() == Status.BOT:
                currentValue = __getCurrentBranchValue(previousBranch, j)
                currentBranch[j] = currentValue + 1
                botValue = max(botValue, currentBranch[j])
            elif cellPlayer.getStatus() == Status.PLAYER:
                currentValue = __getCurrentBranchValue(previousBranch, i)
                currentBranch[i] = currentValue + 1
                playerValue = max(playerValue, currentBranch[i])
        previousBranch = currentBranch

    return botValue - playerValue

def __getCurrentBranchValue(branch: dict, index: int) -> int:
    leftValue = branch[index] if index in branch else 0
    rightValue = branch[index + 1] if index + 1 in branch else 0
    return max(leftValue, rightValue)