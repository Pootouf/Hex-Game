from gi.overrides.Gdk import Color

from src.entity import Board


class Bot(object):
    nextMove : {int, int}
    color : Color

    def __init__(self, color, nextMove):
        self.color = color
        self.nextMove = nextMove

    def getColor(self) -> Color :
        return self.color

    def getNextMove(self) -> {int, int}:
        return self.nextMove

    def calculateNextMove(self, board:Board, difficultyLevel:int):
        #   TODO : method
        self.nextMove = self.getNextMove()