from typing import List

from src.entity.HexGame import HexGame
from src.entity.tree import NodeType
from typing_extensions import Self


class Node(object):
    value: int

    type: NodeType

    parent: Self

    savedMoves: list

    game: HexGame

    def __init__(self):
        self.children = []
        self.parent = None

    def getNodeNumber(self) -> int:
        return len(self.children)

    def getSavedMoves(self) -> list:
        return self.savedMoves

    def isLeaf(self) -> bool:
        return len(self.children) == 0

    def getType(self) -> NodeType:
        return self.type

    def getChildren(self) -> List[Self]:
        return self.children

    def getParent(self) -> Self:
        return self.parent

    def getChild(self, index: int) -> Self:
        return self.children[index]

    def getValue(self) -> int:
        return self.value

    def getGame(self) -> HexGame:
        return self.game

    def addChild(self, child: Self):
        self.children.append(child)
        child.parent = self

    def setType(self, nodeType: NodeType):
        self.type = nodeType

    def setValue(self, nodeValue: int):
        self.value = nodeValue

    def setParent(self, parent: Self):
        self.parent = parent

    def setSavedMoves(self, savedMoves: list):
        self.savedMoves = savedMoves

    def setGame(self, game: HexGame):
        self.game = game