class Position:
    xBoundry = 6
    yBoundry = 6
    lowerBoundry = 1
    x = 0
    y = 0
    direction = ""
    

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def increaseX(self):
        if self.x + 1 <= self.xBoundry:
            self.x += 1
    def increaseY(self):
        if self.y + 1 <= self.yBoundry:
            self.y += 1
    def decreaseX(self):
        if self.x - 1 >= self.lowerBoundry:
            self.x -= 1
    def decreaseY(self):
        if self.y - 1 >= self.lowerBoundry:
            self.y -= 1

class Directions:
    north = "north"
    south = "south"
    east = "east"
    west = "west"
