from dataclasses import dataclass


@dataclass
class Button:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def over(self, pos):
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True
