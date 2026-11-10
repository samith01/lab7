# Lab 7 - Drawbot arm controller.
# Reads a gcode file and plays the moves on the 3 servos of the arm:
#   G1 S<shoulder> E<elbow> -> move those joints to the given angles
#   M3 -> pen down, M5 -> pen up
# The file is played top to bottom, the arm ends wherever the file ends.

from servo_translator import translate
from machine import PWM, Pin
import time

# Each servo is a PWM output on its own GPIO pin (0, 1, 2).
# 50Hz is the standard hobby servo frequency: one pulse every 20ms.
wristServo = PWM(Pin(2))
wristServo.freq(50)

elboServo = PWM(Pin(1))
elboServo.freq(50)

shoulderServo = PWM(Pin(0))
shoulderServo.freq(50)

# True from the moment the pen lifts until it touches back down.
# The first joint move after a pen-up should glide back into place
# instead of snapping there at full speed.
resetting = False


def servoMove(servo, angle):
    # move one servo to a target angle (degrees)
    if resetting and servo != shoulderServo:
        # sweep through the intermediate angles so the arm returns slowly.
        # the shoulder just goes straight to its angle,
        # the elbow is what needs the gentle motion on the way back
        for i in range(10, angle):
            servo.duty_u16(translate(i))
            time.sleep(0.1)

    # translate() converts the angle into the duty_u16 value for that angle
    servo.duty_u16(translate(angle))


with open("circle.gcode", "r") as f:
    for line in f:
        time.sleep(0.1)
        command = line.strip().split()
        print(command)

        # pen up
        if command[0] == "M5":
            servoMove(wristServo, 0)
            resetting = True

        # pen down, arm is back in drawing mode
        if command[0] == "M3":
            servoMove(wristServo, 30)
            resetting = False

        # joint move: S is the shoulder angle, E is the elbow angle.
        # [1:] cuts the letter off the front so float() can parse the number
        if command[0] == "G1":
            shoulderAngle = float(command[1][1:])
            servoMove(shoulderServo, shoulderAngle)

            elboAngle = float(command[2][1:])
            servoMove(elboServo, elboAngle)

        # anything else in the file (like M18 at the end) is ignored
