from enum import Enum


def getHeuristicSelectionFromInt(value: int):
    match value:
        case 1 : return HeuristicSelection.BASIC
        case 2 : return HeuristicSelection.TWO_DISTANCE


class HeuristicSelection(Enum):
    BASIC=1,
    TWO_DISTANCE=2

