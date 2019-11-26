from bot import Bot
from position import Directions, Position
import logging
class Game:
    bots = {}

    def __init__(self):
        logging.info("Initializing positions")
        self.bots["black"] = Bot("green", Position.lowerBoundry, Position.lowerBoundry, Directions.east)
        self.bots["blue"] = Bot("blue", Position.lowerBoundry, Position.yBoundry, Directions.south)
        self.bots["yellow"] = Bot("yellow", Position.xBoundry, Position.yBoundry, Directions.west)
        self.bots["red"] =  Bot("red", Position.xBoundry, Position.lowerBoundry, Directions.north)
        for bot in self.bots:
            logging.info(f"{bot} x: {self.bots[bot].position.x}, y: {self.bots[bot].position.y}")
            

    def move(self, move, color):
        logging.info(f"Moving {color} {move}. From: {self.bots[color].position.x}, {self.bots[color].position.y}, {self.bots[color].position.direction}")
        forward = "forward"
        backword = "backword"
        left = "left"
        right = "right"
        if move == forward:
            if self.bots[color].position.direction == Directions.east:
                self.bots[color].position.increaseX()
            elif self.bots[color].position.direction == Directions.west:
                self.bots[color].position.decreaseX()
            elif self.bots[color].position.direction == Directions.north:
                self.bots[color].position.increaseY()
            elif self.bots[color].position.direction == Directions.south:
                self.bots[color].position.decreaseY() 
        elif move == backword:
            if self.bots[color].position.direction == Directions.east:
                self.bots[color].position.decreaseX()
            elif self.bots[color].position.direction == Directions.west:
                self.bots[color].position.increaseX()
            elif self.bots[color].position.direction == Directions.north:
                self.bots[color].position.decreaseY()
            elif self.bots[color].position.direction == Directions.south:
                self.bots[color].position.increaseY()               
        elif move == left:
            if self.bots[color].position.direction == Directions.east:
                self.bots[color].position.direction = Directions.north
                self.move(forward, color)
            elif self.bots[color].position.direction == Directions.west:
                self.bots[color].position.direction = Directions.south
                self.move(forward, color)
            elif self.bots[color].position.direction == Directions.north:
                self.bots[color].position.direction = Directions.west
                self.move(forward, color)
            elif self.bots[color].position.direction == Directions.south:
                self.bots[color].position.direction = Directions.east
                self.move(forward, color)
        elif move == right:
            if self.bots[color].position.direction == Directions.east:
                self.bots[color].position.direction = Directions.south
                self.move(forward,color)
            elif self.bots[color].position.direction == Directions.west:
                self.bots[color].position.direction = Directions.north
                self.move(forward,color)
            elif self.bots[color].position.direction == Directions.north:
                self.bots[color].position.direction = Directions.east
                self.move(forward,color)
            elif self.bots[color].position.direction == Directions.south:
                self.bots[color].position.direction = Directions.west
                self.move(forward,color)
        logging.info(f"Moved To: {self.bots[color].color} x: {self.bots[color].position.x}, y: {self.bots[color].position.y}, {self.bots[color].position.direction}")

