#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import class_arm
import class_menutext

# Create your objects here.
ev3 = EV3Brick()
bot = class_arm.Arm(Port.C, Port.B, Port.A, Port.S1, Port.S2, Port.S3)
anzeige = class_menutext.Menutext(ev3)
      
# Write your program here.
# Initialisierung Variablen

menubild = False
kalib_sensor_bild = False
menustate = 0
kalibstate = 0

#Ausführen des Programmes

while True:
    #Erstkalibrierung
    if menustate == 0:
        if not kalib_sensor_bild:
            anzeige.anzeigetext(["Kalibriere Sensor", "Endposition oben", "anfahren!", "",  "Speichern: Taste"])
            kalib_sensor_bild = True
        bot.kalibrierung_light()
        if bot.taster.pressed():
            bot.ambient_end = bot.end1.ambient()
            menustate = 3
            
    #Hauptmenuführung
    if menustate == 1:
        if not menubild:
            anzeige.anzeigetext(["Menu", "", "UP: Hand", "LEFT: Kalibrierung", "DOWN: Automatik"])
            menubild = True
        
        #Menuführung: In Handbetrieb wechseln        
        if Button.UP in ev3.buttons.pressed():
            menustate = 2
            anzeige.anzeigetext(["Handbetrieb aktiv", "", "Zurück: Taster"])
            wait(1000)
        
        #Menuführung: Neukalibrierung     
        elif Button.LEFT in ev3.buttons.pressed():
            menustate = 0
            wait(1000)
            
        #Menuführung: In Automatikbetrieb wechseln    
        elif Button.DOWN in ev3.buttons.pressed():
            menustate = 4
            anzeige.anzeigetext(["Automatikbetrieb aktiv", "", "Transport: Taster", "", "Zurück: Center"])
            wait(1000)
                       
    #Handbetrieb
    elif menustate == 2:
        bot.handbetrieb()
        if bot.taster.pressed():
            menustate = 1
            menubild = False
    
    #Kalibrierung      
    elif menustate == 3:
        #Startposition definieren
        if kalibstate == 0:
            wait(1500)
            anzeige.anzeigetext(["Startposition:", "Greifer schliessen", "", "Zum Bestätigen", "Taster drücken"])
            kalibstate = 1  
        elif kalibstate == 1:
            bot.handbetrieb()
            if bot.taster.pressed():
                anzeige.anzeigetext(["Position wird", "gespeichert"])
                wait(1500)
                bot.angle_rl_a = bot.rightleft.angle()
                bot.angle_du_a = bot.downup.angle()
                bot.angle_greiferzu = bot.greifer.angle()
                kalibstate = 2
                
        #Endposition definieren
        elif kalibstate == 2:
            anzeige.anzeigetext(["Endposition:", "Greifer öffnen", "", "Zum Bestätigen", "Taster drücken"])
            kalibstate = 3
        elif kalibstate == 3:
            bot.handbetrieb()
            if bot.taster.pressed():
                anzeige.anzeigetext(["Position wird", "gespeichert"])
                wait(1500)
                bot.angle_rl_b = bot.rightleft.angle()
                bot.angle_du_b = bot.downup.angle()
                bot.angle_greiferauf = bot.greifer.angle()
                kalibstate = 4
        
        #Kalibrierung verlassen
        elif kalibstate == 4:
            anzeige.anzeigetext(["Kalibrierung", "abgeschlossen", "", "Zurück: Taster"])
            kalibstate = 5
        elif kalibstate == 5:
            if bot.taster.pressed():
                kalibstate = 0
                menustate = 1
                menubild = False
    
    #Automatikbetrieb           
    elif menustate == 4:
        bot.automatik()
        if Button.CENTER in ev3.buttons.pressed():
            menustate = 1
            menubild = False