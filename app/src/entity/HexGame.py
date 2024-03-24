from src.entity import Player, Board
from src.entity.Bot import Bot


class HexGame(object):
    isGameFinished:bool
    difficultyLevel:int
    player:Player
    board:Board
    bot:Bot

    def __init__(self, difficultyLevel:int, player:Player, board:Board, bot: Bot):
        self.difficultyLevel = difficultyLevel
        self.player = player
        self.board = board
        self.isGameFinished = False
        self.bot = bot

    def isGameFinished(self) -> bool:
        return self.isGameFinished

    def getDifficultyLevel(self) -> int:
        return self.difficultyLevel

    def getPlayer(self) -> Player:
        return self.player

    def getBoard(self) -> Board:
        return self.board

    def getBot(self) -> Bot:
        return self.bot