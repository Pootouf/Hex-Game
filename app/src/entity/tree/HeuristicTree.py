from src.entity.tree.Node import Node


class HeuristicTree(object):

    def __init__(self, root: Node):
        self.root = root

    def getRoot(self) -> Node:
        return self.root

