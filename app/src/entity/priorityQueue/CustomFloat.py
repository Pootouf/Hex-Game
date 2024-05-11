from typing import Self


class CustomFloat :

    value: float

    def getValue(self):
        return self.value

    def __init__(self, value: float):
        self.value = value


    def __lt__(self, obj: Self):
        """self < obj."""
        return self.value > obj.value


    def __eq__(self, obj: Self):
        """self == obj."""
        return self.value == obj.value

