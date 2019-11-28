# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3

print('Starting up...')
print('Loading EV3 dependencies...')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering, MoveDifferential, MoveTank
from ev3dev2.wheel import EV3Tire
from ev3dev2.button import Button
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.power import PowerSupply

steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
STUD_MM = 8
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)
steering_drive.on(0, SpeedPercent(0))
print('Motors initialized')

print('Loading ROS and other dependencies...')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json
from time import sleep
from math import degrees
import threading
import datetime
from random import uniform

class EV3DEV(object):
    def __init__(self):
        self.exit = True
        self.callback_exit = True
        # Connect sensors and buttons.
        self.btn = Button()
        self.ir = InfraredSensor()
        self.ts = TouchSensor()
        self.power = PowerSupply()
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        print('EV3 Node init starting')
        rospy.init_node('ev3_robot', anonymous=True, log_level=rospy.DEBUG)
        print('EV3 Node init complete')
        rospy.Subscriber('ev3/active_mode', String, self.active_mode_callback, queue_size=1)
        self.power_init()
        print('READY!')


    def active_mode_callback(self, data):
        try:
            rospy.logdebug('Active mode: {}'.format(data))
            self.active_mode = data.data
            self.check_thread()
            if data.data == 'charge':
                thread = self.ir_init()
                sleep(1)
                self.charge(100, 15)
                thread.do_run = False
                thread.join()
            elif data.data == 'halt':
                self.halt()
            elif data.data == 'return':
                self.return_home()
            elif data.data == 'square':
                self.square()
            elif data.data == 'snake':
                self.snake()
            elif data.data == 'spin':
                self.spin()
            elif data.data == 'tracking':
                self.ros_drive('tracking', 'cmd_vel')
                sleep(1)
                self.halt()
            elif data.data == 'joystick':
                self.ros_drive('joystick', 'ev3/cmd_vel')
        except Exception as e:
          rospy.logdebug(e)

    def power_init(self):
        thread = threading.Thread(target=self.power_thread, args=("task",))
        thread.daemon = True
        thread.start()
        return thread

    def power_thread(self, arg):
        while True:
            try:
                print('{} V'.format(self.power.measured_voltage/1000000))
                print('{} A'.format(self.power.measured_current/1000000))
                sleep(2)
            except Exception as e:
                rospy.logdebug(e)
                break

    def ir_init(self):
        thread = threading.Thread(target=self.ir_sensor_thread)
        thread.daemon = True
        thread.start()
        return thread

    def ir_sensor_thread(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            self.distance = self.ir.proximity
            sleep(0.2)
        print("Stopping IR thread...")

    def check_thread(self):
        while not self.exit:
            sleep(0.5)
        while not self.callback_exit:
            sleep(0.5)

    def charge(self, speed, min_distance):
        while self.distance > min_distance:
            self.tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))
        self.halt()

    def square(self):
        for i in range(0,4):
            self.tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2)
            self.tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), 0.94)
        self.halt()

    def snake(self):
        self.halt()
        turn1 = 60
        turn2 = 30
        t = 0.3
        for i in range(0,3):
            # "on" function used here with sleep in order to not stop between
            # steps and has a smooth transition
            self.tank_drive.on(SpeedPercent(turn1), SpeedPercent(turn2))
            sleep(t)
            self.tank_drive.on(SpeedPercent(turn2), SpeedPercent(turn1))
            sleep(t)
            self.tank_drive.on(SpeedPercent(turn2), SpeedPercent(turn1))
            sleep(t)
            self.tank_drive.on(SpeedPercent(turn1), SpeedPercent(turn2))
            sleep(t)
        self.tank_drive.on(SpeedPercent(0), SpeedPercent(0))

    def spin(self):
        speed = 100
        t = 4
        self.tank_drive.on_for_seconds(SpeedPercent(-speed), SpeedPercent(speed), t)
        self.tank_drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(-speed), t)
        self.halt()

    def halt(self):
        self.tank_drive.on(SpeedPercent(0), SpeedPercent(0))

    def return_home(self):
        self.tank_drive.on_for_rotations(SpeedPercent(-50), SpeedPercent(-50), 6)
        self.halt()

    def random_turn(self):
        self.tank_drive.on(SpeedPercent(-50), SpeedPercent(-50))
        sleep(0.8)
        t = uniform(0, 2)
        self.tank_drive.on(SpeedPercent(50), SpeedPercent(-50))
        sleep(t)

    def ros_drive(self, action, topic):
        thread = threading.Thread(target=self.ros_drive_thread, args=(action, topic))
        thread.daemon = True
        thread.start()
        return thread

    def ros_drive_thread(self, action, topic):
        self.exit = False
        sub = rospy.Subscriber(topic, Twist, self.ros_drive_callback)
        while self.active_mode == action:
            sleep(0.5)
        sub.unregister()
        print('topic {} unregistered'.format(topic))
        self.halt()
        self.exit = True

    def ros_drive_callback(self, data):
        try:
            print('x: {} z: {}'.format(data.linear.x, data.angular.z))
            self.callback_exit = False
            x = data.linear.x
            z = data.angular.z

            default_speed = 20
            speed_factor = 100
            turn_factor = 0.628
            if self.ts.is_pressed:
                self.random_turn()
            else:
                if x == 0 and z != 0:
                    if z > 0:
                        print('left')
                        mdiff.turn_left(SpeedPercent(default_speed), degrees(abs(z)), brake=False, block=False)
                    elif z < 0:
                        print('right')
                        mdiff.turn_right(SpeedPercent(default_speed), degrees(abs(z)), brake=False, block=False)
                elif x > 0:
                    print('forward')
                    steering_drive.on(degrees(z)*turn_factor, SpeedPercent(x*speed_factor))
                elif x < 0:
                    print('backward')
                    steering_drive.on(degrees(z)*turn_factor, SpeedPercent(x*speed_factor))
                elif x == 0 and z == 0:
                    print('stop')
                    steering_drive.on(0, SpeedPercent(0))
            self.callback_exit = True
        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        while True:
            try:
                print('Getting ROS Master state...')
                state = rospy.get_master().getSystemState()
                break
            except Exception as e:
                print(e)
                print('ROS Master signal not found, retrying...')
                sleep(2)
        e = EV3DEV()
        while True:
            try:
                state = rospy.get_master().getSystemState()
                sleep(2)
            except Exception as e:
                print(e)
                print('ROS Master signal lost, shutting down...\n\n')
                break
    except Exception as e:
        print(e)
