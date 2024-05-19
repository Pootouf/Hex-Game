from src.entity import Board
from src.entity.Player import Player


class Bot(Player):
    color:str

    def __init__(self, color):
        super().__init__(color)

    def getColor(self) -> str:
        return self.color