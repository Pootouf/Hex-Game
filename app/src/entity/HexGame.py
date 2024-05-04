from src.entity import Player, Board
from src.entity.Bot import Bot
from src.entity.HeuristicSelection import HeuristicSelection
from src.entity.AlgorithmSelection import AlgorithmSelection

class HexGame(object):
    isGameFinished:bool
    difficultyLevel:int
    selectedHeuristic:HeuristicSelection
    selectedAlgorithm:AlgorithmSelection
    player:Player
    board:Board
    bot:Bot

    def __init__(self, difficultyLevel:int, player:Player, board:Board, bot: Bot,
                 selectedHeuristic: HeuristicSelection, selectedAlgorithm: AlgorithmSelection):
        self.difficultyLevel = difficultyLevel
        self.player = player
        self.board = board
        self.isGameFinished = False
        self.bot = bot
        self.selectedHeuristic = selectedHeuristic
        self.selectedAlgorithm = selectedAlgorithm

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

    def getSelectedHeuristic(self) -> HeuristicSelection:
        return self.selectedHeuristic

    def getSelectedAlgorithm(self) -> AlgorithmSelection:
        return self.selectedAlgorithm