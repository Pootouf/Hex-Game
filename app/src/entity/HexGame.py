from app.src.entity import Player, Board


class HexGame(object):
    isGameFinished:bool
    difficultyLevel:int
    player:Player
    board:Board

    def __init__(self, difficultyLevel:int, player:Player,board:Board):
        self.difficultyLevel = difficultyLevel
        self.player = player
        self.board = board
        self.isGameFinished = False

    def isGameFinished(self) -> bool:
        return self.isGameFinished

    def getDifficultyLevel(self) -> int:
        return self.difficultyLevel

    def getPlayer(self) -> Player:
        return self.player

    def getBoard(self) -> Board:
        return self.board

