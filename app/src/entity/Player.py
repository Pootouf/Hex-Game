from gi.overrides.Gdk import Color


class Player(object):
    color:Color

    def __init__(self, color:Color):
        self.color = color

    def getColor(self) -> Color:
        return self.color

    