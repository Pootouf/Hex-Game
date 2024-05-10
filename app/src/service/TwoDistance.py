import math
from heapq import heappop, heappush

from src.entity.Board import Board
from src.entity.Status import Status
from src.service.BasicHeuristic import calculateHeuristicValueForBoard


def calculateHeuristicValueWithTwoDistance(board: Board) -> int:
    # find the player that's closer to winning
    p1_dist = __twoDistanceValueForPlayer(board, Status.PLAYER)
    p2_dist = __twoDistanceValueForPlayer(board, Status.BOT)
    val = p1_dist - p2_dist
    # if a player does not have a 2-distance path, pick a high finite number, so we dont confuse it with a
    # definite win or a definite loss
    if math.isinf(val):
        val = int(math.copysign(100, val))
        val += calculateHeuristicValueForBoard(board)
    if math.isnan(val):
        # if neither player has a path to their opposite side, we get nan
        # in this rare case, revert to normal heuristic
        val = calculateHeuristicValueForBoard(board)
    return val

def __twoDistanceValueForPlayer(board: Board, player: Status) -> float:
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

            if board_val == Status.NONE and (next_row, next_col) not in searched:
                if best_neighbor[next_row][next_col] is None:
                    best_neighbor[next_row][next_col] = neighbor
                elif best_neighbor[next_row][next_col] != neighbor:
                    searched.add((next_row, next_col))
                    heappush(searchq, (dist + 1, next_col if player == Status.PLAYER else next_row, next_row, next_col, (next_row, next_col)))

            elif board_val == player and (next_row, next_col) not in searched:
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
        return math.inf