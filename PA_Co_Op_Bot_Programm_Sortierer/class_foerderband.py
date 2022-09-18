#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

class Foerderband:

    def __init__(self, object, port1, port2, port3, port4):
        """
        Inputs:
        port1 (ColorSensor1), port2 (ColorSensor2),
        port3 (Förderbandmootor), port4 (Sortiermotor)
        """
        self.fs1 = ColorSensor(port1)
        self.fs2 = ColorSensor(port2)
        self.fband = Motor(port3)
        self.sort = Motor(port4)
        self.ev3 = object
        self.kugel_ontheway = False
        self.richtung = 0
    
    #Handbetrieb für Förderband
    def hand_band(self):
        if Button.DOWN in self.ev3.buttons.pressed():
            self.fband.run(120)
        elif Button.UP in self.ev3.buttons.pressed():
            self.fband.run(-120)
        else:
            self.fband.hold()
    
    #Speichert je nach übergebenem String den Winkel einer Position.
    def angle_save(self, position):
        """ Input:
                possible input String: Förderband (down, up) Sortierer(middle, right, left)
                left = gutes Fach / right = schlechtes Fach
            Returns:
                Speicherung erfolgreich(True)
        """
        if position == "down":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.angle_down = self.fband.angle()
                wait(1000)
                return True
            else:
                return False
        elif position == "up":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.angle_up = self.fband.angle()
                wait(1000)
                self.fband.run_target(-120, self.angle_down)
                return True
            else:
                return False
        elif position == "middle":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.sort.reset_angle(0)
                self.angle_middle = self.sort.angle()
                wait(1000)
                return True
            else:
                return False
        elif position == "right":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.angle_right = self.sort.angle()
                wait(1000)
                return True
            else:
                return False
        elif position == "left":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.angle_left = self.sort.angle()
                wait(1000)
                self.richtung = self.shortway(60, self.angle_middle, self.angle_left)
                self.sort.run_target(self.richtung, self.angle_middle)
                self.sort.stop()
                return True
            else:
                return False
    
    #Handbetrieb für Sortierer
    def hand_sort(self):
        if Button.DOWN in self.ev3.buttons.pressed():
            self.sort.run(50)
        elif Button.UP in self.ev3.buttons.pressed():
            self.sort.run(-50)
        else:
            self.sort.hold()
     
    #Farbe von Farbsensor 1 ausgeben und Bestätigung, dass abgespeichert wurde.    
    def kalib_sensor(self, sensor):
        """ Input:
                String: sensor1 (gut), sensor2 (schlecht), sensor3
            Returns:
                Speicherung erfolgreich(True), Farbe(Color.BLACK...etc. or None)
        """
        if sensor == "sensor1":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.kugel_ok = self.fs1.reflection()
                wait(1000)
                return True
            else:
                return False
        elif sensor == "sensor2":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.kugel_bad = self.fs1.reflection()
                wait(1000)
                return True
            else:
                return False
        elif sensor == "sensor3":
            if Button.CENTER in self.ev3.buttons.pressed():
                self.kugel_any = self.fs2.reflection()
                wait(1000)
                return True
            else:
                return False

    #Funktion zur Bestimmung der kürzeren Richtung
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
    
    #Automatischer Transport
    def automatik(self):
        if self.fs1.reflection() > 0:
            if (self.fs1.reflection() <= (self.kugel_ok + 5)) and ((self.kugel_ok-5) <= self.fs1.reflection()):
                self.richtung = 1
                self.fband.run_target(100, self.angle_up)
                self.fband.run_target(-100, self.angle_down)
                self.kugel_ontheway = True
            elif (self.fs1.reflection()<= (self.kugel_bad + 5)) and ((self.kugel_bad -5) <= self.fs1.reflection()):
                self.richtung = 2
                self.fband.run_target(100, self.angle_up)
                self.fband.run_target(-100, self.angle_down)
                self.kugel_ontheway = True
            else:
                self.fband.hold()
        
        if self.kugel_ontheway == True:
            if self.fs2.reflection() * 2 >= self.kugel_any:
                if self.richtung == 1:
                    self.richtung = self.shortway(60, self.angle_left, self.angle_middle)
                    self.sort.run_target(self.richtung, self.angle_left)
                    self.sort.run_target(-self.richtung, self.angle_middle)
                    self.kugel_ontheway = False
                    return True
                elif self.richtung == 2:
                    self.richtung = self.shortway(60, self.angle_right, self.angle_middle)
                    self.sort.run_target(self.richtung, self.angle_right)
                    self.sort.run_target(-self.richtung, self.angle_middle)
                    self.kugel_ontheway = False
                    return True
            else:
                self.sort.stop()
            

    
