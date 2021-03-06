#!/usr/bin/python

# from .models import Mitbewohni,Ausgabe,Ausgleichszahlung
from decimal import Decimal
import operator
from .models import Ausgabe


def summiereAusgaben(ausgaben):
    summe_ausgaben = 0
    for ausgabe in ausgaben:
        summe_ausgaben += ausgabe.wert
    return summe_ausgaben

def getMBWAusgaben(MBW,ausgaben,agzs):
    dummy_ausgaben = 0
    for ausgabe in ausgaben:
        if MBW.username == ausgabe.mitbewohni.username:
            dummy_ausgaben += ausgabe.wert
    for agz in agzs:
        if MBW.username == agz.von.username:
            dummy_ausgaben += agz.wert
        if MBW.username == agz.an.username:
            dummy_ausgaben -= agz.wert
    return dummy_ausgaben

def getMBWAusgabenDJANGO(mitbewohnis=[],ausgaben=[],agzs=[]):
    MBW_ausgaben = []
    for MBW in mitbewohnis:
        dummy_ausgaben = getMBWAusgaben(MBW,ausgaben,agzs)
        MBW_ausgaben.append((MBW.username,dummy_ausgaben))
    return MBW_ausgaben

def getNoetigeAusgleichszahlungen(mitbewohnis,ausgaben=[],agzs=[]):
    book = {}
    for mitbewohni in mitbewohnis:                                      #Alle Mitbewohnis erhalten einen Saldoeintrag = 0
        book[mitbewohni] = 0
    for ausgabe in ausgaben:                                            #Saldoberechnung AUSG - Jede Ausgabe wird einem mitbewohni als Kredit zugeordnet (Anteil * Anzahl der anderen MBWs)
        ausgabe_mbws = ausgabe.an.all()
        ausgabe.wert = float(ausgabe.wert)
        anteil = ausgabe.wert / len(ausgabe_mbws)
        for mitbewohni in ausgabe_mbws:
            if mitbewohni == ausgabe.mitbewohni:
                book[mitbewohni] += (ausgabe.wert - anteil)
            else:
                book[mitbewohni] -= anteil
    noetige_agzs = []
    for mitbewohni in mitbewohnis:
        if book[mitbewohni] < 0:
            while abs(book[mitbewohni]) >= 0.01:                        #in der elif Bedinung kann Schuldbetrag uU != 0 bleiben. Daher diese Bedingung
                largest_creditor = max(book, key=lambda key: book[key])
                if abs(book[mitbewohni]) <= book[largest_creditor]:     #Schuldbetrag ist kleiner als der Betrag der dem größten Gläubiger geschuldet wird
                    if abs(book[mitbewohni]) > 0.01:
                        f = abs(book[mitbewohni])
                        d = round(Decimal(f),2)
                        noetige_agzs.append((mitbewohni,largest_creditor,d))
                    book[largest_creditor] += book[mitbewohni]
                    book[mitbewohni] = 0
                elif abs(book[mitbewohni]) > book[largest_creditor]:    #Schuldbetrag ist größer als der Betrag der dem größten Gläubiger geschuldet wird
                    if book[largest_creditor] > 0.01:
                        f = abs(book[largest_creditor])
                        d = round(Decimal(f),2)
                        noetige_agzs.append((mitbewohni,largest_creditor,d))
                    book[mitbewohni] += book[largest_creditor]
                    book[largest_creditor] = 0
                else:
                    print("FEHLER IN NOETIGE AGZS!!!")
                    noetige_agzs.append("FEHLER IN NOETIGE AGZS!!!")
                    break
    return noetige_agzs

def getStartDatum():
    erste_ausgabe = Ausgabe.objects.all().order_by("datum")[0]
    return erste_ausgabe.datum

def getEndDatum():
    letzte_ausgabe = Ausgabe.objects.all().order_by("-datum")[0]
    return letzte_ausgabe.datum

#Testumgebung
if __name__ == "__main__":

    class Ausgabe():


        def __init__(self, datum, wert, mitbewohni,an,notiz):

            self.datum = datum
            self.wert = wert
            self.mitbewohni = mitbewohni
            self.an = an
            self.notiz = notiz

    class Mitbewohni():

        def __init__(self,name,mail):
            self.username = name
            self.mail = mail

    class Ausgleichszahlung():

        def __init__(self,von_mitbewohni,an_mitbewohni,wert,datum):
            self.von = von_mitbewohni
            self.an = an_mitbewohni
            self.wert = wert
            self.datum = datum

    m1 = Mitbewohni("Jess","jess@richie.nk")
    m2 = Mitbewohni("Moritz","jess@richie.nk")
    m3 = Mitbewohni("Lue","jess@richie.nk")

    mitbewohnis = [m1,m2,m3]
    an1 = [m1,m2,m3]
    an2 = [m1,m3]

    a1 = Ausgabe("date",30,m1,an1,"leer")
    a2 = Ausgabe("date",20,m2,an2,"leer")
    a3 = Ausgabe("date",30,m3,an1,"leer")

    ausgaben = [a1,a2,a3]

    ag1 = Ausgleichszahlung(m1,m2,56.88,"leer")
    ag2 = Ausgleichszahlung(m3,m1,20.66,"leer")

    agzs = [ag1,ag2]

    # getAnteil(ausgaben,3)
    getNoetigeAusgleichszahlungen(mitbewohnis,ausgaben)

