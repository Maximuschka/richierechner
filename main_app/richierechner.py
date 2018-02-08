#!/usr/bin/python

# from .models import Mitbewohni,Ausgabe,Ausgleichszahlung
from decimal import Decimal
import operator
from .models import Ausgabe,Ausgleichszahlung

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

def getNoetigeAusgleichszahlungen2(mitbewohnis,ausgaben=[],agzs=[]):
    book = {}
    for mitbewohni in mitbewohnis:                                  #Alle Mitbewohnis erhalten einen Salodeintrag = 0
        book[mitbewohni] = 0
    for ausgabe in ausgaben:                                        #Jede Ausgabe wird einem mitbewohni als Kredit zugeordnet (Anteil * Anzahl der anderen MBWs)
        ausgabe.wert = float(ausgabe.wert)
        anteil = ausgabe.wert / len(mitbewohnis)
        book[ausgabe.mitbewohni] += anteil * (len(mitbewohnis)-1)
        for mitbewohni in mitbewohnis:                              #Jede Ausgabe wird den verbleibenden mitbewohnis als anteilige Schuld zugeordnet
            if mitbewohni != ausgabe.mitbewohni:
                book[mitbewohni] -= anteil
                book[mitbewohni] = book[mitbewohni]
    for agz in agzs:                                                #Jede agz wird als Kredit bzw. Schuld dem jeweilige mitbewohni zugeordnet
        book[agz.von] += float(agz.wert)
        book[agz.an] -= float(agz.wert)
    noetige_agzs = []
    for mitbewohni in mitbewohnis:
        print("1")
        if book[mitbewohni] < 0:
            print("2")
            while abs(book[mitbewohni]) >= 0.01:
                largest_creditor = max(book, key=lambda key: book[key])
                print(abs(book[mitbewohni]))
                print(book[largest_creditor])

                if abs(book[mitbewohni]) <= book[largest_creditor]:
                    print("3")
                    if abs(book[mitbewohni]) > 0.01:
                        f = abs(book[mitbewohni])
                        d = round(Decimal(f),2)
                        noetige_agzs.append((mitbewohni,largest_creditor,d))
                    book[largest_creditor] += book[mitbewohni]
                    book[mitbewohni] = 0
                elif abs(book[mitbewohni]) > book[largest_creditor]:
                    print("4")
                    if book[largest_creditor] > 0.01:
                        f = abs(book[largest_creditor])
                        d = round(Decimal(f),2)
                        noetige_agzs.append((mitbewohni,largest_creditor,d))
                    book[mitbewohni] += book[largest_creditor]
                    book[largest_creditor] = 0
                else:
                    print("FEHLER IN NOETIGE AGZS!!!")
    print(book)
    print(noetige_agzs)
    return noetige_agzs

# def getNoetigeAusgleichszahlungenDJANGO(mitbewohnis=[],ausgaben=[],agzs=[]):
#     agzs = getNoetigeAusgleichszahlungen(mitbewohnis,ausgaben,agzs)

#     agzsDJANGO = []

#     for agz in agzs:
#         if agz[1] != agz[2]:
#             if agz[0] > 0:
#                 agzsDJANGO.append((agz[2].username,agz[1].username,agz[0]))
#             elif agz[0] < 0:
#                 agzsDJANGO.append((agz[1].username,agz[2].username,agz[0]*(-1)))
#     return agzsDJANGO

# def getNoetigeAusgleichszahlungen(mitbewohnis=[],ausgaben=[],agzs=[]):

#     """Berechnet die nötigen Ausgleichsszahlungen. Werte kleiner als 5 Cent werden vernachlässigt."""

#     saldo = getSaldoListe(mitbewohnis,ausgaben,agzs)
#     ausgleichszahlungen = []
#     for item in saldo:
#         if item[0] > 0:
#             zahlung = (item[0])
#             item[0] = 0
#             saldo[-1][0] += zahlung
#             ausgleichszahlungen.append((zahlung,item[1],saldo[-1][1]))
#         elif item[0] < 0:
#             zahlung = item[0]
#             item[0] = 0
#             saldo[-1][0] -= zahlung
#             ausgleichszahlungen.append((zahlung,item[1],saldo[-1][1]))
#     return ausgleichszahlungen

# def getSaldoListe(mitbewohnis,ausgaben,agzs):
#     saldo = []
#     c = len(mitbewohnis)
#     for MBW in mitbewohnis:
#         saldo.append([getSaldoMBW(MBW,ausgaben, agzs, c),MBW])
#     return sorted(saldo, key =  lambda x: x[0], reverse=True)

# def getSaldoMBW(MBW, ausgaben, agzs, c):
#     MBW_ausgaben = getMBWAusgaben(MBW, ausgaben, agzs)
#     anteil = getAnteil(ausgaben,c)
#     return MBW_ausgaben - anteil
    
#     return self.getMBWAusgaben(MBW)-self.getAnteil(summiereAusgaben(ausgaben))

# def getAnteil(ausgaben,c):
#     return round(summiereAusgaben(ausgaben)/c,2)

def getStartDatum():
    erste_ausgabe = Ausgabe.objects.all().order_by("datum")[0]
    return erste_ausgabe.datum

def getEndDatum():
    letzte_ausgabe = Ausgabe.objects.all().order_by("-datum")[0]
    return letzte_ausgabe.datum

#Testumgebung
if __name__ == "__main__":

    class Ausgabe():


        def __init__(self, datum, wert, mitbewohni,notiz):

            self.datum = datum
            self.wert = wert
            self.mitbewohni = mitbewohni
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

    a1 = Ausgabe("date",18.15,m1,"leer")
    a2 = Ausgabe("date",7.93,m2,"leer")
    a3 = Ausgabe("date",67,m3,"leer")

    ausgaben = [a1,a2,a3]

    ag1 = Ausgleichszahlung(m1,m2,56.88,"leer")
    ag2 = Ausgleichszahlung(m3,m1,20.66,"leer")

    agzs = [ag1,ag2]

    # getAnteil(ausgaben,3)
    getNoetigeAusgleichszahlungen2(mitbewohnis,ausgaben,agzs)

