import math
from random import random

from src.entity.Board import Board
from src.entity.Bot import Bot
from src.entity.Cell import Cell
from src.entity.HexGame import HexGame
from src.entity.Player import Player
from src.entity.Status import Status
from src.entity.tree.HeuristicTree import HeuristicTree
from src.entity.tree.Node import Node
from src.entity.tree.NodeType import NodeType


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


def createHeuristicTree(board: Board, height: int) -> HeuristicTree:
    node = Node()
    node.setType(Status.PLAYER)

    heuristicTree = HeuristicTree(node)
    __addChildNodes(node, board, height, Status.BOT)
    return heuristicTree


def applyMinimax(tree: HeuristicTree):
    root = tree.getRoot()
    __minimax(root, tree)


def __addChildNodes(root: Node, board: Board, height: int, activePlayer: Status):
    if height == 0:
        root.setValue(__calculateHeuristicValueForBoard(board))
        return
    for i in range(board.getSideLength()):
        for j in range(board.getSideLength()):
            if board.getCell(i, j).getStatus() != Status.NONE:
                continue
            node = Node()
            node.setType(activePlayer)
            root.addChild(node)
            newBoard = __getNewBoardWithSelectedAction(board, i, j, activePlayer)
            __addChildNodes(node, newBoard, height - 1, __getActivePlayer(activePlayer))


def __getActivePlayer(currentActivePlayer: Status) -> Status:
    match currentActivePlayer:
        case Status.NONE:
            return Status.NONE
        case Status.PLAYER:
            return Status.BOT
        case Status.BOT:
            return Status.PLAYER


def __getNewBoardWithSelectedAction(currentBoard: Board, x: int, y: int, activePlayer: Status) -> Board:
    cells = currentBoard.getCells().copy()
    cells[x][y].setStatus(activePlayer)
    return Board(cells)


def __calculateHeuristicValueForBoard(board: Board) -> int:
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


def __minimax(root: Node, tree: HeuristicTree) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    if root.getType() == NodeType.MAX:
        val = - math.inf
        for k in range(bf):
            val = max(val, __minimax(root.getChild(k), tree))
    else:
        val = math.inf
        for k in range(bf):
            val = min(val, __minimax(root.getChild(k), tree))
    return val
