#Libraries
import RPi.GPIO as GPIO
import time
import os
from recorder import Pibot

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 11

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    print ("calculating distance")
    # set Trigger after 0.01ms to LOW
    time.sleep(1)
    print("time")
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    print(StopTime)

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        print("save start time")
        StartTime = time.time()

        #print(StartTime)

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        print("save stop time")
        StopTime = time.time()
        print(StopTime)

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    print(TimeElapsed)
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print(distance)
    return distance

if __name__ == '__main__':
    try:
        while True:
            print ("starting now")
            dist = distance()
            print (dist)
            print ("Measured Distance = %.1f cm" % dist)
            if 60 <= dist <= 150:
                cmd = "ffplay -nodisp -autoexit /home/pi/PolyglotRobot/Initialflow/recordafterthetone.mp3 "
                os.system(cmd)
                cmd2="python3 /home/pi/PolyglotRobot/Initialflow/led.py &"
                os.system(cmd2)
                pibot = Pibot()
                pibot.startListening()
                print("After listening")
                #os.system(cmd2)
                cmd3="kill -9 `ps -ef| grep 'led' | awk '{print $2}'`"
                os.system(cmd3)
            else:
                print ("No person detected")
                cmd2="python3 /home/pi/PolyglotRobot/Initialflow/moveNeck.py"
                os.system(cmd2)

            time.sleep(5)


        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
