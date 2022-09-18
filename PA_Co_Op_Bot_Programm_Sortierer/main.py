#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import class_menutext
import class_foerderband

# Create your objects here.
ev3 = EV3Brick()
anzeige = class_menutext.Menutext(ev3)
sorter = class_foerderband.Foerderband(ev3, Port.S1, Port.S4, Port.B, Port.D)

# Write your program here.

menustate = 0
text_schreiben = False
verzoegerung = 0
process = False

while True:
   
    #Position Förderband unten definieren
    if menustate == 0:
        if not text_schreiben:
            anzeige.anzeigetext(["Kalibrierung", "Förderband", "", "Position unten", "", "Save: CENTER"])
            text_schreiben = True
        sorter.hand_band()
        if sorter.angle_save("down"):
            menustate = 1
            text_schreiben = False
    
    #Position Förderband oben definieren        
    if menustate == 1:
        if not text_schreiben:
            anzeige.anzeigetext(["Kalibrierung", "Förderband", "Position oben", "", "", "Save: CENTER"])
            text_schreiben = True
        sorter.hand_band()
        if sorter.angle_save("up"):
            menustate = 2
            text_schreiben = False
        
    #Auf Position unten fahren und Objektfarbe auslesen    
    elif menustate == 2:
        anzeige.anzeigetext(["Kalibrierung", "Sensorwert:", sorter.fs1.reflection(), "Objekt Gut", "", "Save: CENTER"])
        wait(50)
        if sorter.kalib_sensor("sensor1"):
            menustate = 3
            text_schreiben = False
            
    #Objektfarbe auslesen    
    elif menustate == 3:
        anzeige.anzeigetext(["Kalibrierung", "Sensorwert:", sorter.fs1.reflection(), "", "Objekt Bad", "Save: CENTER"])
        wait(50)
        if sorter.kalib_sensor("sensor2"):
            menustate = 4
            text_schreiben = False
    
    #Sortierer auf Grundposition
    elif menustate == 4:
        if not text_schreiben:
            anzeige.anzeigetext(["Kalibrierung", "Sortierer in", "Grundposition", "", "", "Save: CENTER"])
            text_schreiben = True
        sorter.hand_sort()
        if sorter.angle_save("middle"):
            menustate = 5
            text_schreiben = False
    
    #Sortierer auf Grundposition
    elif menustate == 5:
        anzeige.anzeigetext(["Kalibrierung", "Sortierer in", "schlechtes Fach", sorter.sort.angle(), "", "Save: CENTER"])
        wait(50)
        sorter.hand_sort()
        if sorter.angle_save("right"):
            menustate = 6
    
    #Sortierer auf Grundposition
    elif menustate == 6:
        anzeige.anzeigetext(["Kalibrierung", "Sortierer in", "gutes Fach", sorter.sort.angle(), "", "Save: CENTER"])
        wait(50)
        sorter.hand_sort()
        if sorter.angle_save("left"):
            menustate = 7
    
    #Objekt erkennen    
    elif menustate == 7:
        
        anzeige.anzeigetext(["Kalibrierung", sorter.fs2.reflection(), "Objekt mit", "niedrigem Wert", "vor Sortiersensor", "Save: CENTER"])
        wait(50)
        if sorter.kalib_sensor("sensor3"):
            menustate = 10
            
    #Hauptmenu
    elif menustate == 10:
        if not text_schreiben:
            anzeige.anzeigetext(["Menu:", "", "Automatik: LEFT", "Kalibrieren: RIGHT"])
            text_schreiben = True
        elif Button.LEFT in ev3.buttons.pressed():
            menustate = 15
            text_schreiben = False
        elif Button.RIGHT in ev3.buttons.pressed():
            menustate = 0
            text_schreiben = False
        
    #Automatikbetrieb aufrufen
    elif menustate == 15:
        wait(100)
        anzeige.anzeigetext(["Automatikbetrieb", sorter.fs1.reflection(), "Abbruch: CENTER"])
        if sorter.fs1.reflection() > 0:
            verzoegerung += 1
            if verzoegerung >= 20:
                process = sorter.automatik()
                if process == True:
                    verzoegerung = 0
                    process = False
        if Button.CENTER in ev3.buttons.pressed():
            menustate = 10
            verzoegerung = 0