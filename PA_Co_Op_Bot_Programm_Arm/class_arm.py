#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Create your objects here.
ev3 = EV3Brick()

class Arm:
    def __init__(self, port1, port2, port3, port4, port5, port6):
        """
        Inputs:
        port1 (Zentraler Drehmotor), port2 (Armotor für up down), port3 (Greifermotor)
        port4 (Farbsensor, Endschalter), port5 (Endschalter Drehmotor), port6 (Zusatztaster)
        """
        self.rightleft = Motor(port1)
        self.downup = Motor(port2)
        self.greifer = Motor(port3)
        self.end1 = ColorSensor(port4)
        self.end2 = TouchSensor(port5)
        self.taster = TouchSensor(port6)
        self.angle_rl_a = 0
        self.angle_rl_b = 0
        self.angle_du_a = 0
        self.angle_du_b = 0
        self.angle_greiferauf = 0
        self.angle_greiferzu = 0
        self.greiferstate = False
        self.greiferpressed = False
        self.speedm = 100
        self.speedg = 50
        self.speed_auto = 0
        self.ambient_end = 0

    #Handbetrieb über EV3 Tasten
    def handbetrieb(self):
        """
        Bedienung erfolgt über Tasten auf EV3.
        """
        if Button.RIGHT in ev3.buttons.pressed() and not(self.end2.pressed()):
            self.rightleft.run(100)
        elif Button.LEFT in ev3.buttons.pressed():
            self.rightleft.run(-100)
        elif Button.DOWN in ev3.buttons.pressed():
            self.downup.run(100)
        elif Button.UP in ev3.buttons.pressed() and self.end1.ambient() > self.ambient_end:
            self.downup.run(-100)
        elif Button.CENTER in ev3.buttons.pressed():
            self.greiferpressed = True
            if self.greiferstate == False:
                self.greifer.run(50)
            elif self.greiferstate == True:
                self.greifer.run(-50)
        else:
            self.rightleft.hold()
            self.downup.hold()
            self.greifer.stop()
            if self.greiferpressed == True:
                self.greiferstate = not(self.greiferstate)
                self.greiferpressed = False

    #Teil der Automatikfunktion, küzeren Winkel ermitteln.
    def shortway(self, speed, angle_a, angle_b):
        """
        speed (Motorgeschwindigkeit), angle_a (die gewünschte Endposition), angle_b (die Anfangsposition)
        Nicht auf Start und Endpunkt bezogen sondern auf die gewünschte Bewegung. 
        """
        if (angle_a - angle_b) <= (angle_b - angle_a):
            speedtemp = -speed
        else:
            speedtemp = speed
        return (speedtemp)

    #Teil der Automatikfunktion. Grundposition, Arm ist in der Greifposition mit dem Arm ganz oben.
    def startposition(self):
        self.speed_auto = self.shortway(self.speedm, self.angle_rl_a, self.angle_rl_b)
        self.rightleft.run_target(self.speed_auto, self.angle_rl_a)
        while self.end1.ambient() > self.ambient_end:
            self.downup.run(-self.speedm)
        self.downup.hold()
        self.speed_auto = self.shortway(self.speedg, self.angle_greiferauf, self.angle_greiferzu)
        self.greifer.run_target(self.speed_auto, self.angle_greiferauf)
    
    #Teil der Automatikfunktion (automatische Bewegung des Armes)
    def transport(self):
        self.speed_auto = self.shortway(self.speedm, self.angle_du_a, self.angle_du_b)
        self.downup.run_target(self.speed_auto, self.angle_du_a)
        self.speed_auto = self.shortway(self.speedg, self.angle_greiferzu, self.angle_greiferauf)
        self.greifer.run_target(self.speed_auto, self.angle_greiferzu)
        self.speed_auto = self.shortway(self.speedm, self.angle_du_b, self.angle_du_a)
        self.downup.run_target(self.speed_auto, self.angle_du_b)
        self.speed_auto = self.shortway(self.speedm, self.angle_rl_b, self.angle_rl_a)
        self.rightleft.run_target(self.speed_auto, self.angle_rl_b)
        self.speed_auto = self.shortway(self.speedg, self.angle_greiferauf, self.angle_greiferzu)
        self.greifer.run_target(self.speed_auto, self.angle_greiferauf)

    #Autmatikfunktion ausführen
    def automatik(self):
        self.startposition()
        if self.taster.pressed():
            self.transport()
            wait(1000)
     
    #Lichtsensor kalibrieren       
    def kalibrierung_light(self):
        if Button.DOWN in ev3.buttons.pressed():
            self.downup.run(100)
        elif Button.UP in ev3.buttons.pressed():
            self.downup.run(-100)
        else:
            self.downup.hold()