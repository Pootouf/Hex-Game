from src.entity import Board
from src.entity.Player import Player


class Bot(Player):
    nextMove : {int, int}

    def __init__(self, color):
        super().__init__(color)


    def getNextMove(self) -> {int, int}:
        return self.nextMove

    def calculateNextMove(self, board:Board, difficultyLevel:int):
        #   TODO : method
        self.nextMove = self.getNextMove()