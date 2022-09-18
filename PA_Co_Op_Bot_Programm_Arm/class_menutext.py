
# Create your objects here.

class Menutext:
    def __init__(self, object):
        self.ev3_1 = object
        
    def anzeigetext(self, liste):
        """_Beschreibung_
        Anzeigetext als Liste ("textzeile1", textzeile2, ...) übergeben.
        Jeder Text wird in einer separaten Zeile ausgegeben.
        """
        zeile = 0
        self.ev3_1.screen.clear()
        self.text_liste = liste
        for i in self.text_liste:
            self.ev3_1.screen.draw_text(0, zeile, str(i))
            zeile += 20