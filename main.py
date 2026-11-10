from servo_translator import translate
from machine import PWM,Pin
import time

wristServo = PWM(Pin(2))
wristServo.freq(50)

elboServo = PWM(Pin(1))
elboServo.freq(50)

shoulderServo = PWM(Pin(0))
shoulderServo.freq(50)


def servoMove(servo,angle):
    if resetting and servo != shoulderServo:
        for i in range(10,angle):
            servo.duty_u16(translate(i))
            time.sleep(0.1)
        
    servo.duty_u16(translate(angle))
    
resetting = False

with open("circle.gcode", "r") as f:
    for line in f:   
        time.sleep(0.1)
        command = line.strip().split()
        print(command)
        
        if command[0] == "M5":
            servoMove(wristServo,0) #up
            resetting = True
            
        if command[0] == "M3":
            servoMove(wristServo,30)
            resetting = False
        
        if command[0] == "G1":
            shoulderAngle = float(command[1][1:])
            servoMove(shoulderServo,shoulderAngle)
            
            elboAngle = float(command[2][1:]) 
            servoMove(elboServo,elboAngle)
        
            
        
