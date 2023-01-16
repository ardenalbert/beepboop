# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import pwmio
from adafruit_motor import servo
from micropython import const
from Adafruit_seesaw.seesaw import Seesaw

BUTTON_RIGHT = const(6)
BUTTON_DOWN = const(7)
BUTTON_LEFT = const(9)
BUTTON_UP = const(10)
BUTTON_SEL = const(14)
button_mask = const(
    (1 << BUTTON_RIGHT)
    | (1 << BUTTON_DOWN)
    | (1 << BUTTON_LEFT)
    | (1 << BUTTON_UP)
    | (1 << BUTTON_SEL)
)

i2c_bus = board.I2C()

ss = Seesaw(i2c_bus)

ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)

# create a PWMOut object on the control pin.
xpwm = pwmio.PWMOut(board.A2, duty_cycle=0, frequency=50)
ypwm = pwmio.PWMOut(board.A3, duty_cycle=0, frequency=50)
lbpwm = pwmio.PWMOut(board.A4, duty_cycle=0, frequency=50)
rbpwm = pwmio.PWMOut(board.SCK, duty_cycle=0, frequency=50)

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo. The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo = servo.Servo(board.D5, actuation_range=135)
xservo = servo.Servo(xpwm, min_pulse=700, max_pulse=2300)
yservo = servo.Servo(ypwm, min_pulse=700, max_pulse=2300)
lbservo = servo.Servo(lbpwm, min_pulse=500, max_pulse=2500)
rbservo = servo.Servo(rbpwm, min_pulse=500, max_pulse=2500)

last_x = 0
last_y = 0

def shake_head():
    xservo.fraction = 0.2
    time.sleep(0.2)
    xservo.fraction = 0.4
    time.sleep(0.2)
    xservo.fraction = 0.2
    time.sleep(0.2)
    xservo.fraction = 0.4
    time.sleep(0.2)
    xservo.fraction = 0.3
    time.sleep(0.2)

#def simones_gesture():
    #Simones gesture code here

def wonder():
    lbservo.fraction = 0.3
    rbservo.fraction = 0.7
    time.sleep(0.2)

def neutral():
    lbservo.fraction = 0.5
    rbservo.fraction = 0.5
    time.sleep(0.2)

def angry():
    lbservo.fraction = 0.7
    rbservo.fraction = 0.3
    time.sleep(0.2)

while True:
    x = ss.analog_read(2)
    y = ss.analog_read(3)

    if (abs(x - last_x) > 3) or (abs(y - last_y) > 3):
        #call joystick move function here
        xfraction = (x/1023)
        yfraction = (y/1023)
        xservo.fraction = xfraction
        yservo.fraction = yfraction
        print(x, y)
        print(xfraction, yfraction)
        last_x = x
        last_y = y

    buttons = ss.digital_read_bulk(button_mask)
    if not buttons & (1 << BUTTON_RIGHT):
        #call button A function
        shake_head()
        print("Button A pressed")

    if not buttons & (1 << BUTTON_DOWN):
        print("Button B pressed")
        #call button B function
        #simones_gesture()

    if not buttons & (1 << BUTTON_LEFT):
        #call button Y function
        wonder()
        print("Button Y pressed")

    if not buttons & (1 << BUTTON_UP):
        #call button x function
        neutral()
        print("Button x pressed")

    if not buttons & (1 << BUTTON_SEL):
        #call button SEL function
        angry()
        print("Button SEL pressed")

    time.sleep(0.01)
