
from rpi_ws281x import *
import math
import logging
strip = None
colors = {
    "blue":     Color(0,0,255),
    "red":      Color(255,0,0),
    "green":    Color(0,255,0),
    "yellow":   Color(207,245,66),
    "amazon":   Color(102,17,0),
    "gray":     Color(32,32,32),
    "black":    Color(0,0,0)
}

## x,y correlation to LED board
ledMatrix = {
    1: { 1: 785, 2: 790, 3: 795, 4: 699,  5: 694, 6: 689 },
    2: { 1: 865, 2: 870, 3: 875, 4: 619,  5: 614, 6: 609 },
    3: { 1: 945, 2: 950, 3: 955, 4: 539,  5: 534, 6: 529 },
    4: { 1: 17,  2: 22,  3: 27,  4: 443,  5: 438, 6: 433 },
    5: { 1: 97, 2: 102, 3: 107, 4: 363,  5: 358, 6: 353 },
    6: { 1: 177, 2: 182, 3: 187, 4: 283,  5: 278, 6: 273 }
}

border=[
  list(range(752,784)),
  list(range(240,273)),
  list(range(15,1024,32)),
  list(range(16,1024,32))
]
grid=[list(range(0,16)), 
          list(range(496,528)),
          list(range(1008,1024)),
          list(range(0,1024,32)),
          list(range(31,1024,32)),
          list(range(5,1024,16)),
          list(range(10,1024,16)),
          list(range(81,97)),
          list(range(161,177)),
          list(range(336,352)),
          list(range(416,432)),
          list(range(593,609)),
          list(range(673,689)),
          list(range(849,865)),
          list(range(929,945))
          ]

rows=[list(range(5,1024,5))]
class Board:
    def __init__(self):
        logging.info("Initializing Game Board")
        LED_COUNT =         1024
        LED_PIN =           18
        LED_FREQ_HZ =       800000
        LED_DMA =           10
        LED_BRIGHTNESS =    125
        LED_INVERT =        False
        LED_CHANNEL =       0
        self.strip = PixelStrip(LED_COUNT, 
                                LED_PIN, 
                                LED_FREQ_HZ, 
                                LED_DMA,
                                LED_INVERT, 
                                LED_BRIGHTNESS, 
                                LED_CHANNEL)
        self.strip.begin()
        logging.info("Creating Border")
        self.light(border,colors["amazon"])
        logging.info("Creating Grid")
        self.light(grid,colors["gray"])


    def light(self, section, color):
        for pointRange in section:
            for point in pointRange:
                self.strip.setPixelColor(point,color)
        self.strip.show()
    
    def lightPosition(self, x, y, color):
        logging.info(f"lighting {x}, {y} color: {color}")
        self.light(self.getSquare(ledMatrix[x][y]), colors[color])

    def unlightPosition(self, x, y):
        self.lightPosition(x, y, "black")
    
    def getSquare(self, number):
        square = []
        row = math.ceil(number/16)
        rowEnd = row*16
        rowStart = (row-1)*16
        positionFromStart = number - rowStart
        positionFromEnd = rowEnd - number
 
        for nextRow in range(row,row+4):
            logging.debug(f"Next Row: {nextRow}")
            if nextRow % 2 == 0:
                square.append(list(range(((nextRow*16)-16) +  positionFromStart, ((nextRow*16)-16) + positionFromStart + 4)))
            else:
                square.append(list(range(((nextRow*16)-16) + positionFromEnd - 4 , ((nextRow*16)-16) + positionFromEnd)))
        return square




