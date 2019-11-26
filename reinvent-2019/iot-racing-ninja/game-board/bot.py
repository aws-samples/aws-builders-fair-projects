from position import Position
class Bot:
    color = ""
    position = None
    def __init__(self, color, x, y, direction):
        self.position = Position(x, y, direction)
        self.color = color