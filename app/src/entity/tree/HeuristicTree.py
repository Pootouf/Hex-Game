from src.entity.tree.Node import Node


class HeuristicTree(object):

    node_count: int

    def __init__(self, root: Node):
        self.root = root
        self.node_count = 1

    def getRoot(self) -> Node:
        return self.root

