import math
from heapq import heappop, heappush
from queue import Queue
from enum import Enum
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
from src.entity.HeuristicSelection import *
from src.entity.AlgorithmSelection import *


def createGame(boardSize: int, difficultyLevel: int, heuristicChoice: int, algorithmChoice: int) -> HexGame:
    cells = []
    for i in range(boardSize):
        cellList = []
        for j in range(boardSize):
            cellList.append(Cell(i, j, Status.NONE))
        cells.append(cellList)
    board = Board(cells)

    player = Player("blue")
    bot = Bot("red")
    heuristic = getHeuristicSelectionFromInt(heuristicChoice)
    algorithm = getAlgorithmSelectionFromInt(algorithmChoice)
    return HexGame(difficultyLevel, player, board, bot, heuristic, algorithm)


def createHeuristicTree(game: HexGame, height: int) -> HeuristicTree:
    node = Node()
    node.setType(Status.PLAYER)
    __addChildNodes(node, game, list(), height, Status.BOT)

    heuristicTree = HeuristicTree(node)
    return heuristicTree


def applyMinimax(tree: HeuristicTree):
    root = tree.getRoot()
    __minimax(root)


def applyNegamax(tree: HeuristicTree):
    root = tree.getRoot()
    __negamax(root)


def applyAlphaBeta(tree: HeuristicTree):
    root = tree.getRoot()
    __alphabeta(root, -math.inf, math.inf)


def applyNegAlphaBeta(tree: HeuristicTree):
    root = tree.getRoot()
    __negAlphaBeta(root, -math.inf, math.inf)

def playOneMove(cell: Cell, game: HexGame):
    cell.setStatus(Status.PLAYER)
    heuristictree = createHeuristicTree(game, game.difficultyLevel)
    match game.selectedAlgorithm:
        case AlgorithmSelection.MINIMAX: applyMinimax(heuristictree)
        case AlgorithmSelection.NEGAMAX: applyNegamax(heuristictree)
        case AlgorithmSelection.ALPHABETA: applyAlphaBeta(heuristictree)
        case AlgorithmSelection.NEGALPHABETA: applyNegAlphaBeta(heuristictree)
        case AlgorithmSelection.SSS: applySSS(heuristictree)

    maxNode = None
    for child in heuristictree.root.getChildren():
        if maxNode is None or maxNode.getValue() < child.getValue():
            maxNode = child

    game.board.getCell(maxNode.getSavedMoves()[0][0], maxNode.getSavedMoves()[0][1]).setStatus(Status.BOT)


def applySSS(tree: HeuristicTree):
    root = tree.getRoot()
    __sss(root)



def __addChildNodes(root: Node, game: HexGame, savedMoves: list, height: int, activePlayer: Status):
    if height == 0:
        newBoard = __copyBoard(game.board)
        for (x, y, status) in savedMoves:
            newBoard.getCell(x, y).setStatus(status)

        match game.selectedHeuristic:
            case HeuristicSelection.BASIC:
                root.setValue(__calculateHeuristicValueForBoard(newBoard))
            case HeuristicSelection.TWO_DISTANCE:
                root.setValue(__calculateHeuristicValueWithTwoDistance(newBoard, activePlayer))

        return

    board = game.board
    for i in range(board.getSideLength()):
        for j in range(board.getSideLength()):
            if (board.getCell(i, j).getStatus() != Status.NONE
                    or (i, j, Status.BOT) in savedMoves or (i, j, Status.PLAYER) in savedMoves):
                continue
            node = Node()
            node.setType(activePlayer)
            root.addChild(node)
            newMoves = savedMoves.copy()
            newMoves.append((i, j, activePlayer))
            node.setSavedMoves(newMoves)
            __addChildNodes(node, game, newMoves, height - 1, __getActivePlayer(activePlayer))


def __getActivePlayer(currentActivePlayer: Status) -> Status:
    match currentActivePlayer:
        case Status.NONE:
            return Status.NONE
        case Status.PLAYER:
            return Status.BOT
        case Status.BOT:
            return Status.PLAYER


def __copyBoard(currentBoard: Board) -> Board:
    newTab = []
    for row in currentBoard.getCells():
        newRow = []
        for cell in row:
            newRow.append(cell.copy())
        newTab.append(newRow)
    return Board(newTab)


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


def __calculateHeuristicValueWithTwoDistance(board: Board, player: Status) -> int:
    sideLength = board.getSideLength()
    if player == Status.PLAYER:
        searchq = [(0, sideLength, i, sideLength, (i, sideLength)) for i in range(-1, sideLength)]
    else:
        searchq = [(0, sideLength, sideLength, i, (sideLength, i)) for i in range(-1, sideLength)]
    best_neighbor = [[None] * board.getSideLength() for _ in range(board.getSideLength())]
    best_opposite = None
    searched = set()
    dist = -1
    connected = False
    while searchq:
        dist, weight, row, col, neighbor = heappop(searchq)

        if weight == 0:
            if best_opposite is None:
                best_opposite = neighbor
            elif best_opposite != neighbor:
                connected = True
                break

        for dy, dx in [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]:
            next_row = row + dy
            next_col = col + dx

            # efficiency optimization. faster than checking if the cell is out of bounds
            try:
                if next_row < 0 or next_col < 0:
                    continue
                else:
                    board_val = board.getCells()[next_row][next_col].getStatus()
            except IndexError:
                continue

            if board_val == Status.BOT and (next_row, next_col) not in searched:
                if best_neighbor[next_row][next_col] is None:
                    best_neighbor[next_row][next_col] = neighbor
                elif best_neighbor[next_row][next_col] != neighbor:
                    searched.add((next_row, next_col))
                    heappush(searchq, (dist + 1, next_col if player == Status.PLAYER else next_row, next_row, next_col, (next_row, next_col)))

            elif board_val == Status.PLAYER and (next_row, next_col) not in searched:
                if best_neighbor[next_row][next_col] is None:
                    best_neighbor[next_row][next_col] = neighbor
                    heappush(searchq, (dist, next_col if player == Status.PLAYER else next_row, next_row, next_col, neighbor))
                elif best_neighbor[next_row][next_col] != neighbor:
                    searched.add((next_row, next_col))
                    best_neighbor[next_row][next_col] = neighbor
                    heappush(searchq, (dist, next_col if player == Status.PLAYER else next_row, next_row, next_col, neighbor))


    # once the search is finished, build the list of the shortest path
    if connected:
        return dist
    # if there is no way to reach the other side, treat it as infinite distance
    else:
        return int("max")


def __getCurrentBranchValue(branch: dict, index: int) -> int:
    leftValue = branch[index] if index in branch else 0
    rightValue = branch[index + 1] if index + 1 in branch else 0
    return max(leftValue, rightValue)


"""
    minimax: return the minimax value of the tree's root
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __minimax(root: Node) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    if root.getType() == NodeType.MAX:
        val = - math.inf
        for k in range(bf):
            val = max(val, __minimax(root.getChild(k)))
    else:
        val = math.inf
        for k in range(bf):
            val = min(val, __minimax(root.getChild(k)))
    root.setValue(val)
    return val


"""
    negamax: return the negamax value of the tree's root
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __negamax(root: Node) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    val = - math.inf
    for k in range(bf):
        val = max(val, - __negamax(root.getChild(k)))
    root.setValue(val)
    return val


"""
    negAlphaBeta: return the negamax value of the tree's root by applying NegAlphaBeta algorithm
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __negAlphaBeta(root: Node, alpha: float, beta: float) -> float:
    if root.isLeaf():
        return root.getValue()
    bf: int = len(root.getChildren())
    k: int = 0
    val: float = - math.inf
    while alpha < beta and k < bf:
        val = max(val, - __negAlphaBeta(root.getChild(k), -beta, -alpha))
        alpha = max(alpha, val)
        k += 1
    return val


def __alphabeta(root: Node, alpha: float, beta: float) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    else:
        if root.getType() == NodeType.MAX:
            k: int = 0
            while alpha < beta and k < bf:
                alpha = max(alpha, __alphabeta(root.getChild(k), alpha, beta))
                k += 1
            root.setValue(alpha)
            return alpha
        else:
            k: int = 0
            while alpha < beta and k < bf:
                beta = min(beta, __alphabeta(root.getChild(k), alpha, beta))
                k += 1
            root.setValue(beta)
            return beta


def __sss(root: Node) -> float:
    k: int
    G = Queue[(Node, NodeState, int)]()
    G.put((root, NodeState.V, float('inf')))
    while G.queue[0][1] is not NodeState.R and G.queue[0][0] is not root:
        tup = G.queue.popleft()
        if tup[1] == NodeState.V:
            if tup[0].isLeaf():
                G.put((tup[0], NodeState.R, min(tup[2], tup[0].value)))
            else:
                if tup[0].nodeType == NodeType.MAX:
                    for i in range(1, len(tup[0].getChildren())):
                        G.put((tup[0].getChild(i), NodeState.V, tup[2]))
                else:
                    G.put((__getLeftmostUndiscoveredSucc(tup[0]), NodeState.V, tup[2]))
        else:
            if tup[0].nodeType == NodeType.MIN:
                G.put((tup[0].getParent(), NodeState.R, tup[2]))
                tup[0].setValue(tup[2])
                for t in G.queue:
                    if t[0].getParent() is tup[0].getParent():
                        G.get(t)
            else:
                sibling = __getUndiscoveredRightSibling(tup[0])
                if sibling is not None:
                    G.put((sibling, NodeState.V, tup[2]))
                else:
                    G.put((tup[0].getParent(), NodeState.R, tup[2]))
                    tup[0].setValue(tup[2])
    resolvedTup = G.queue.popleft()
    root.setValue(resolvedTup[2])
    return resolvedTup[2]


"""
    getLeftmostUndiscoveredSucc: return the node at the leftmost of the tree with inf value
    :param node, the node where to find the leftmost node: 
    :return the node at the leftmost of the tree with inf value: 
"""


def __getLeftmostUndiscoveredSucc(node: Node) -> Node | None:
    for currentNode in node.getChildren():
        if currentNode.getValue() is float('inf'):
            return currentNode
    return None


"""
   getUndiscoveredRightSibling : return the node at the right of the given node with inf value
   :param node, the node from which we want to find the sibling: 
   :return the first right sibling undiscovered node: 
"""


def __getUndiscoveredRightSibling(node: Node) -> Node | None:
    parent = node.getParent()
    isAtRightOfNode = False
    for currentNode in parent.getChildren():
        if currentNode is node:
            isAtRightOfNode = True
            continue
        else:
            if currentNode.getValue() is float('inf') and isAtRightOfNode:
                return currentNode


class NodeState(Enum):
    V = 0,
    R = 1
