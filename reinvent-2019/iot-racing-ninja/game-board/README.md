# game-board
## Overview
Game Board will subscribe to the MQTT queues the controllers are sending messages to and modify the positions in the board respectively.
## Controler
### Code
In this repo
### Physical
[Rasberry Pi 4 modle B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/ref=sxin_2_ac_d_pm?ac_md=3-0-VW5kZXIgJDUw-ac_d_pm&keywords=raspberry+pi+4&pd_rd_i=B07TD42S27&pd_rd_r=13e557b0-3dbd-402b-bc12-8a48bb651d11&pd_rd_w=pjKmP&pd_rd_wg=OMtJ0&pf_rd_p=02e79b16-eab7-4369-852f-d04a58a4d9b5&pf_rd_r=R78YZQPWRCAXRK397W1P&psc=1&qid=1572011659&rnid=2528832011)
## The Board
### Logical
6x6 2x2 squares
### Phyiscal
[BTF-LIGHTING WS2812B RGB 5050SMD](https://www.amazon.com/gp/product/B01DC0IOCK/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) 
The phyisical (16x16) LED board will divied into 6x6 (2 x 2) sections and a 2 LED border
May possibly increase this to 4 boards (64x64) which would be 10x10 6x6 sections and 2 LED Boarder
## Housing
https://www.homedepot.com/p/Everbilt-16-in-x-16-in-Interconnecting-Plastic-Pegboard-in-Black-50-lbs-17961/202249707
### Adjustments
Drill 3 holes larger a row up and a row down from center. 
## Moves
### Forward
Moves the game peice forward one unit
### Backword
Moves the game peice forward one unit
### Left
Turns left and moves forward
### Right
Turns right and moves forward
### Reset
Reset peices to original positions. 