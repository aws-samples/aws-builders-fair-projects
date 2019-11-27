# game-board
## Running
log in as pi user
```
cd game-board
sudo ./main.py
```
## Updating
```
cd game-board
git pull
```
## Overview
Game Board will subscribe to the MQTT queues the controllers are sending messages to and modify the positions in the board respectively.

### BOM
1 x [rasberry pi 4 Starter Kit](https://www.amazon.com/gp/product/B07V5JTMV9/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1) 
4 x [BTF-LIGHTING WS2812B RGB 5050SMD](https://www.amazon.com/gp/product/B01DC0IOCK/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) 
1 x [5v power supply for LEDs](https://www.amazon.com/gp/product/B01LXN7MN3/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
1 [Breadboard with Rasberry PI GPIO breakout](https://www.amazon.com/gp/product/B072XBX3XX/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)

### Logical setup. 
Once connected the boards are divided into 6 x 6 squares with a 1 row border around the edge and a one row border between each square. 
The LED boards are wired in a snaking fasion, so in order to light up a 4x4 square, the code has to do some inversion of positioning for every other row (if the starting row started 5 positions from the begining of that row, then the next row will need to start 9 (5+4) positions from the end of the next row). 

#### Housing
https://www.homedepot.com/p/Everbilt-16-in-x-16-in-Interconnecting-Plastic-Pegboard-in-Black-50-lbs-17961/202249707
##### Adjustments
Drill 3 holes larger (1/2 in) a row up and a row down from center so that the LED Board wires can be threaded. 
## Process Move
### Forward
Moves the game peice forward one unit
### Backword
Moves the game peice backward one unit. (This functionality is currently not used, but was added here for when it is). 
### Left
Turns left and moves forward
### Right
Turns right and moves forward
## Process Locate
Allows for the manual positioning of vehicles.
## Process Shutdown
Black out all lights. 