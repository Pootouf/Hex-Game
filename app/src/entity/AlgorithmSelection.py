from enum import Enum

def getAlgorithmSelectionFromInt(value: int):
    match value:
        case 1 : return AlgorithmSelection.MINIMAX
        case 2 : return AlgorithmSelection.NEGAMAX
        case 3 : return AlgorithmSelection.ALPHABETA
        case 4 : return AlgorithmSelection.NEGALPHABETA
        case 5 : return AlgorithmSelection.SSS

class AlgorithmSelection(Enum):
    MINIMAX=1,
    NEGAMAX=2,
    ALPHABETA=3,
    NEGALPHABETA=4,
    SSS=5