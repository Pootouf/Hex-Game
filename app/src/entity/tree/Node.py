from typing import List

from src.entity.tree import NodeType
from typing_extensions import Self


class Node(object):
    value: int

    type: NodeType

    def __init__(self):
        self.children = []

    def getNodeNumber(self) -> int:
        return len(self.children)

    def isLeaf(self) -> bool:
        return len(self.children) == 0

    def getType(self) -> NodeType:
        return self.type

    def getChildren(self) -> List[Self]:
        return self.children

    def getChild(self, index: int) -> Self:
        return self.children[index]

    def addChild(self, child: Self):
        self.children.append(child)

    def setType(self, nodeType: NodeType):
        self.type = nodeType

    def setValue(self, nodeValue: int):
        self.value = nodeValue

    def getValue(self) -> int:
        return self.value
