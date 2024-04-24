import math
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


def applyNegamax(tree: HeuristicTree):
    root = tree.getRoot()
    __negamax(root, tree)


def applyAlphaBeta(tree: HeuristicTree):
    root = tree.getRoot()
    __alphabeta(root, tree, -math.inf, math.inf)


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


def __negamax(root: Node, tree: HeuristicTree) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    val = - math.inf
    for k in range(bf):
        val = max(val, - __negamax(root.getChild(k), tree))
    return val


def __alphabeta(root: Node, tree: HeuristicTree, alpha: float, beta: float) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return root.getValue()
    else:
        if root.getType() == NodeType.MAX:
            k: int = 0
            while alpha < beta and k < bf:
                alpha = max(alpha, __alphabeta(root.getChild(k), tree, alpha, beta))
                k += 1
            return alpha
        else:
            k: int = 0
            while alpha < beta and k < bf:
                beta = min(beta, __alphabeta(root.getChild(k), tree, alpha, beta))
                k += 1
            return beta

def __sss(root: Node, tree: HeuristicTree) -> float:
    k: int
    G = Queue[(Node, NodeState, int)]()
    G.put((root,NodeState.V, float('inf')))
    while G.queue[0][1] is not NodeState.R and G.queue[0][0] is not root:
        tup = G.queue.popleft()
        if tup[1] == NodeState.V:
            if tup[0].isLeaf() :
                G.put((tup[0], NodeState.R, min(tup[2], tup[0].value)))
            else :
                if tup[0].nodeType == NodeType.MAX :
                    for i in range(1, len(tup[0].getChildren())) :
                        G.put((tup[0].getChild(i), NodeState.V, tup[2]))
                else :
                    G.put((__getLeftmostUndiscoveredSucc(tup[0]), NodeState.V, tup[2]))
        else :
            if tup[0].nodeType == NodeType.MIN :
                G.put((tup[0].getParent(), NodeState.R, tup[2]))
                for t in G.queue :
                    if t[0].getParent() is tup[0].getParent() :
                        G.get(t)
            else :
                sibling = __getUndiscoveredRightSibling(tup[0])
                if sibling is not None :
                    G.put((sibling, NodeState.V, tup[2]))
                else :
                    G.put((tup[0].getParent(), NodeState.R, tup[2]))
    resolvedTup = G.queue.popleft()
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

 """
    getUndiscoveredRightSibling : return the node at the right of the given node with inf value
    :param node, the node from which we want to find the sibling: 
    :return the first right sibling undiscovered node: 
"""
def __getUndiscoveredRightSibling(node: Node) -> Node | None :
    parent = node.getParent()
    isAtRightOfNode = False
    for currentNode in parent.getChildren() :
        if currentNode is node :
            isAtRightOfNode = True
            continue
        else :
            if currentNode.getValue() is float('inf') and isAtRightOfNode:
                return currentNode


class NodeState(Enum):
    V=0,
    R=1
