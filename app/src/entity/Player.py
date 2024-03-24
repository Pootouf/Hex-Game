
class Player(object):
    color:str

    def __init__(self, color:str):
        self.color = color

    def getColor(self) -> str:
        return self.color

    