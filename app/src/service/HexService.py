import time
import math
from queue import PriorityQueue

from src.entity.Board import Board
from src.entity.Bot import Bot
from src.entity.Cell import Cell
from src.entity.HexGame import HexGame
from src.entity.Player import Player
from src.entity.priorityQueue.CustomFloat import CustomFloat
from src.entity.priorityQueue.PrioritizedItem import PrioritizedItem
from src.entity.Status import Status
from src.entity.tree.HeuristicTree import HeuristicTree
from src.entity.tree.Node import Node
from src.entity.tree.NodeType import NodeType
from src.entity.HeuristicSelection import *
from src.entity.AlgorithmSelection import *
from src.service.BasicHeuristic import calculateHeuristicValueForBoard
from src.service.TwoDistance import calculateHeuristicValueWithTwoDistance
from src.service.WinnerVerification import getWinner

"""
    createGame: create an Hex game
    :param boardSize, the length of the board:
    :param difficultyLevel, the wanted difficulty for the bot actions:
    :param heuristicChoice, the chosen heuristic to use:
    :param algorithmChoice, the chosen algorithm to use:
    :return the created Hex game:
"""


def createGame(boardSize: int, difficultyLevel: int, heuristicChoice: int, algorithmChoice: int) -> HexGame:
    cells = []
    for i in range(boardSize):
        cellList = []
        for j in range(boardSize):
            cell = Cell(i, j, Status.NONE)
            cellList.append(cell)
        cells.append(cellList)
    board = Board(cells)

    player = Player("blue")
    bot = Bot("red")
    heuristic = getHeuristicSelectionFromInt(heuristicChoice)
    algorithm = getAlgorithmSelectionFromInt(algorithmChoice)

    game = HexGame(difficultyLevel, player, board, bot, heuristic, algorithm)

    __initializeCellsNeighbour(game)
    return game


"""
    createHeuristicTree: create the heuristic tree for the game with given depth
    :param game, the current hex game:
    :param height, the height of the wanted tree:
    :return the heuristic tree:
"""


def createHeuristicTree(game: HexGame, height: int) -> HeuristicTree:
    node = Node()
    node.setType(NodeType.MAX)
    node.setGame(game)
    __addChildNodes(node, game, list(), height, Status.BOT)

    heuristicTree = HeuristicTree(node)
    heuristicTree.node_count = __computeHeuristicTreeUnvisitedNodes(node)
    return heuristicTree


"""
    applyMinimax: apply Minimax algorithm to the tree
    :param tree the tree on which the algorithm is applied:
    :return: the heuristic value of the tree's root:
"""


def applyMinimax(tree: HeuristicTree):
    root = tree.getRoot()
    __minimax(root)


"""
    applyNegamax: apply Negamax algorithm to the tree
    :param tree the tree on which the algorithm is applied:
    :return: the heuristic value of the tree's root:
"""


def applyNegamax(tree: HeuristicTree):
    root = tree.getRoot()
    __negamaxHeuristic(root)
    __negamax(root)


"""
    applyAlphaBeta: apply AlphaBeta algorithm to the tree
    :param tree the tree on which the algorithm is applied:
    :return: the heuristic value of the tree's root:
"""


def applyAlphaBeta(tree: HeuristicTree):
    root = tree.getRoot()
    __alphabeta(root, -math.inf, math.inf)


"""
    applyNegAlphaBeta: apply NegAlphaBeta algorithm to the tree
    :param tree the tree on which the algorithm is applied:
    :return: the heuristic value of the tree's root:
"""


def applyNegAlphaBeta(tree: HeuristicTree):
    root = tree.getRoot()
    __negamaxHeuristic(root)
    __negAlphaBeta(root, -math.inf, math.inf)


"""
    playOneMove: play a single move on the Hex Game, for the player like it choose, and one for the bot
    :param cell, the selected cell by the player:
    :param game, the current Hex game:
"""


def playOneMove(cell: Cell, game: HexGame):
    if cell.getStatus() != Status.NONE or game.winner != Status.NONE:
        return
    cell.setStatus(Status.PLAYER)
    winner = getWinner(game.board)
    if winner is not Status.NONE:
        game.setWinner(winner)
        game.setIsGameFinished(True)
        return
    heuristictree = createHeuristicTree(game, game.difficultyLevel)
    start = time.time()
    match game.selectedAlgorithm:
        case AlgorithmSelection.MINIMAX:
            applyMinimax(heuristictree)
            game.addRemoveNodesCount(0)
        case AlgorithmSelection.NEGAMAX:
            applyNegamax(heuristictree)
            game.addRemoveNodesCount(0)
        case AlgorithmSelection.ALPHABETA:
            applyAlphaBeta(heuristictree)
            game.addRemoveNodesCount(__computeHeuristicTreeUnvisitedNodes(heuristictree.root))
        case AlgorithmSelection.NEGALPHABETA:
            applyNegAlphaBeta(heuristictree)
            game.addRemoveNodesCount(__computeHeuristicTreeUnvisitedNodes(heuristictree.root))
        case AlgorithmSelection.SSS:
            applySSS(heuristictree)
            game.addRemoveNodesCount(__computeHeuristicTreeUnvisitedNodes(heuristictree.root))
    end = time.time()
    elapsed_time = (end - start) * 1000
    game.last_time_played = elapsed_time
    __resetVisitedNode(heuristictree.getRoot())
    maxNode = None
    for child in heuristictree.root.getChildren():
        if game.selectedAlgorithm == AlgorithmSelection.NEGALPHABETA or game.selectedAlgorithm == AlgorithmSelection.NEGAMAX:
            if (maxNode is None or not (hasattr(maxNode, "value"))
                    or (hasattr(child, "value") and -maxNode.getValue() < -child.getValue())):
                maxNode = child
        else:
            if (maxNode is None or not (hasattr(maxNode, "value"))
                    or (hasattr(child, "value") and maxNode.getValue() < child.getValue())):
                maxNode = child

    game.board.getCell(maxNode.getSavedMoves()[0][0], maxNode.getSavedMoves()[0][1]).setStatus(Status.BOT)
    getWinner(game.board)
    if winner is not Status.NONE:
        game.setWinner(winner)
        game.setIsGameFinished(True)
        return


"""
    applySSS: apply SSS* algorithm to the tree
    :param tree the tree on which the algorithm is applied:
    :return: the heuristic value of the tree's root:
"""


def applySSS(tree: HeuristicTree):
    root = tree.getRoot()
    __sss(root)


"""
    addChildNodes: creates recursively the nodes of the heuristic tree
    :param root, the root of the heuristic tree:
    :param game, the HexGame instance:
    :param savedMoves, contains the registered moves to reach this node:
    :param height, the height of the tree:
    :param activePlayer, the status of the current player;
    :return: the heuristic value of the tree's root:
"""
def __addChildNodes(root: Node, game: HexGame, savedMoves: list, height: int, activePlayer: Status):
    if height == 0:
        return

    board = game.board
    for i in range(board.getSideLength()):
        for j in range(board.getSideLength()):
            if (board.getCell(i, j).getStatus() != Status.NONE
                    or (i, j, Status.BOT) in savedMoves or (i, j, Status.PLAYER) in savedMoves):
                continue
            node = Node()
            if activePlayer == Status.PLAYER:
                node.setType(NodeType.MAX)
            else:
                node.setType(NodeType.MIN)
            root.addChild(node)
            node.setGame(game)
            newMoves = savedMoves.copy()
            newMoves.append((i, j, activePlayer))
            node.setSavedMoves(newMoves)
            __addChildNodes(node, game, newMoves, height - 1, __getActivePlayer(activePlayer))


"""
    getActivePlayer: return Status of the active player
    :param currentActivePlayer, the current player who played:
    :return the status of the active player:
"""


def __getActivePlayer(currentActivePlayer: Status) -> Status:
    match currentActivePlayer:
        case Status.NONE:
            return Status.NONE
        case Status.PLAYER:
            return Status.BOT
        case Status.BOT:
            return Status.PLAYER


"""
    copyBoard: make a deep copy of the board
    :param currentBoard, the board actually used:
    :return the board copied:
"""


def __copyBoard(currentBoard: Board) -> Board:
    newTab = []
    for row in currentBoard.getCells():
        newRow = []
        for cell in row:
            newRow.append(cell.copy())
        newTab.append(newRow)
    return Board(newTab)


"""
    minimax: return the minimax value of the tree's root
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __minimax(root: Node) -> float:
    bf: int = len(root.getChildren())
    if root.isLeaf():
        return __getValueFromNode(root, root.getGame())
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
        return __getValueFromNode(root, root.getGame())
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
    root.setVisited(True)
    if root.isLeaf():
        return __getValueFromNode(root, root.getGame())
    bf: int = len(root.getChildren())
    k: int = 0
    val = - math.inf
    while alpha < beta and k < bf:
        val = max(val, - __negAlphaBeta(root.getChild(k), -beta, -alpha))
        alpha = max(alpha, val)
        k += 1
    root.setValue(val)
    return val


"""
    alphaBeta: return the alphaBeta value of the tree's root by applying alphaBeta algorithm
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __alphabeta(root: Node, alpha: float, beta: float) -> float:
    bf: int = len(root.getChildren())
    root.setVisited(True)
    if root.isLeaf():
        return __getValueFromNode(root, root.getGame())
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


"""
    sss: return the SSS* value of the tree's root by applying SSS* algorithm
    :param root the root of the tree
    :param tree the tree on which the algorithm is applied
    :return: the heuristic value of the tree's root
"""


def __sss(root: Node) -> float:
    G = PriorityQueue[PrioritizedItem]()
    G.put(PrioritizedItem(CustomFloat(math.inf), (root, NodeState.V)))
    while G.queue[0].item[1] is not NodeState.R or G.queue[0].item[0] is not root:
        tup = G.get()
        state = tup.item[1]
        currentNode = tup.item[0]
        value = tup.priority


        if state == NodeState.V:
            currentNode.setVisited(True)
            if currentNode.isLeaf():
                newValue = min(value.getValue(), float(__getValueFromNode(currentNode, currentNode.getGame())))
                G.put(PrioritizedItem(CustomFloat(newValue),
                                      (currentNode, NodeState.R)))
                currentNode.setValue(newValue)
            else:
                if currentNode.getType() == NodeType.MAX:
                    for i in range(1, len(currentNode.getChildren())):
                        G.put(PrioritizedItem(value, (currentNode.getChild(i), NodeState.V)))
                else:
                    node = __getLeftmostUndiscoveredSucc(currentNode, G)
                    if node is not None:
                        G.put(PrioritizedItem(value, (node, NodeState.V)))
                    else:
                        print("Node not found")

        else:
            currentNode.setValue(value.getValue())
            if currentNode.getType() == NodeType.MIN:
                parent = currentNode.getParent()
                G.put(PrioritizedItem(value, (parent, NodeState.R)))
                parent.setValue(value.getValue())
                H = PriorityQueue[(CustomFloat, (Node, NodeState))]()
                for t in G.queue:
                    if t.item[0].getParent() is not parent:
                        H.put(t)
                G = H
            else:
                sibling = __getUndiscoveredRightSibling(currentNode, G)
                if sibling is not None:
                    G.put(PrioritizedItem(value, (sibling, NodeState.V)))
                else:
                    G.put(PrioritizedItem(value, (currentNode.getParent(), NodeState.R)))
                    currentNode.getParent().setValue(value.getValue())
    resolvedTup = G.queue.pop(0)
    root.setValue(int(resolvedTup.priority.getValue()))
    return resolvedTup.priority.getValue()


"""
    getLeftmostUndiscoveredSucc: return the node at the leftmost of the tree with inf value
    :param node, the node where to find the leftmost node: 
    :return the node at the leftmost of the tree with inf value: 
"""


def __getLeftmostUndiscoveredSucc(node: Node, G: PriorityQueue) -> Node | None:
    copiedQueue = G.queue
    discoveredQueueElements = list(filter(lambda t: t.item[0].getParent() == node, copiedQueue))
    discoveredNodes = list(map(lambda t: t.item[0], discoveredQueueElements))
    for child in node.getChildren():
        if child not in discoveredNodes:
            return child
    return None


"""
   getUndiscoveredRightSibling : return the node at the right of the given node with inf value
   :param node, the node from which we want to find the sibling: 
   :return the first right sibling undiscovered node: 
"""


def __getUndiscoveredRightSibling(node: Node, G: PriorityQueue) -> Node | None:
    parent = node.getParent()
    copiedQueue = G.queue
    discoveredQueueElements = list(filter(lambda t: t.item[0].getParent() == parent, copiedQueue))
    discoveredNodes = list(map(lambda t: t.item[0], discoveredQueueElements))
    isAtRightOfNode = False
    for currentNode in parent.getChildren():
        if currentNode is node:
            isAtRightOfNode = True
            continue
        else:
            if currentNode not in discoveredNodes and isAtRightOfNode:
                return currentNode
    return None



"""
   initializeCellsNeighbour : set the neighbours of each cell according to the Hex Board
   :param game, the game containing hex board: 
"""


def __initializeCellsNeighbour(game: HexGame):
    board = game.board
    boardSize = board.getSideLength()
    for x in range(boardSize):
        for y in range(boardSize):
            cell = board.getCell(x, y)
            if x != 0:
                # add top neighbour
                cell.addNeighbour(board.getCell(x - 1, y))
                if y != boardSize - 1:
                    # add top right neighbour
                    cell.addNeighbour(board.getCell(x - 1, y + 1))
            if y != 0:
                # add left neighbour
                cell.addNeighbour(board.getCell(x, y - 1))
                if x != boardSize - 1:
                    # add bottom left neighbour
                    cell.addNeighbour(board.getCell(x + 1, y - 1))

            if x != boardSize - 1:
                # add bottom neighbour
                cell.addNeighbour(board.getCell(x + 1, y))

            if y != boardSize - 1:
                # add right neighbour
                cell.addNeighbour(board.getCell(x, y + 1))


"""
    negamaxHeuristic: transforms the heuristic of the tree into a negamax
    :param the root of the tree:
"""


def __negamaxHeuristic(root: Node, deepLevel: int = 1):
    if root.isLeaf():
        if deepLevel % 2 == 0:
            root.setValue(- __getValueFromNode(root, root.game))
        return
    else:
        for child in root.getChildren():
            __negamaxHeuristic(child, deepLevel + 1)

"""
    getValueFromNode: return the value of the node depending on the heuristic
    :param node, the node whose value is wanted:
    :param game, the game being played:
"""
def __getValueFromNode(node: Node, game: HexGame) -> int:
    if node.isLeaf():
        if not hasattr(node, "value"):
            newBoard = __copyBoard(game.board)
            for (x, y, status) in node.getSavedMoves():
                newBoard.getCell(x, y).setStatus(status)
            match game.selectedHeuristic:
                case HeuristicSelection.BASIC:
                    node.setValue(calculateHeuristicValueForBoard(newBoard))
                case HeuristicSelection.TWO_DISTANCE:
                    node.setValue(calculateHeuristicValueWithTwoDistance(newBoard))
    return node.getValue()



def __computeHeuristicTreeUnvisitedNodes(node: Node):
    count = 0
    if not node.isVisited():
        count += 1
    for child in node.getChildren():
        count += __computeHeuristicTreeUnvisitedNodes(child)
    return count


def __resetVisitedNode(root: Node):
    root.setVisited(False)
    for child in root.getChildren():
        __resetVisitedNode(child)

class NodeState(Enum):
    V = 0,
    R = 1
