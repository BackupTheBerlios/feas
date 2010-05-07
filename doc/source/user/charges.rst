.. index::
   Geb�hren
   
========
Geb�hren
========
   
Die Geb�hrenabrechnung in FEAS st�tzt sich auf drei S�ulen. Zun�chst ist im Modul "Flugarten" festzulegen, wer mit der Geb�hren-Buchung belastet werden soll. Im darauf aufba�nden Modul "Geb�hren" kann nun festgelegt werden, unter welchen Umst�nden der unter "Flugarten" genannte Zahler belastet wird. 

Das Geb�hrenmodul selbst ist in zwei Tabellen unterteilt. Jeweils eine f�r Startgeb�hren und eine f�r Landegeb�hren. Der Unterschied beider Tabellen ist, dass die Buchung der Startgeb�hren beim Start erfolgt und die Buchung der Landegeb�hren bei der Landung.

Um alle Szenarien des Flugbetriebs erfassen zu k�nnen und um Doppelte Arbeit zu vermeiden verwendet FEAS Python-Skript vorlagen zur Definition der Geb�hren. Dies erscheint Anfangs zwar etwas �bertrieben zu sein, doch nur so ist die Abdeckung aller m�glichen Geb�hren-Szenarien m�glich.

Die Tabellen Startgeb�hren und Landegeb�hren lesen sich wie folgt:
Es ist f�r jede Flugart eine Zeile vorhanden, sowie jeweils eine Spalte f�r die verschiedenen Start-Arten vorhanden ist. Die verf�gbaren Startarten sind Eigenstart, Windenstart und Schleppstart.

Nun ist es m�glich, f�r jede der verschiedenen Flug- und Startarten eine Python-Skriptvorlage zu vergeben. Entweder existiert bereits eine Vorlage (welche bereits f�r eine andere Flug-/Startart angelegt wurde), oder man muss eine ne� Vorlage erstellen.

Um eine Vorlage zu erstellen sind Kenntnisse in der Skriptsprache Python von Vorteil, aber nicht unbedingt notwendig. Im Folgenden wird anhand von Beispielen gezeigt, wie man eigene Geb�hren-Vorlagen erstellen kann und welche M�glichkeiten zur Anpassung bestehen.

Definition einer Geb�hrenvorlage
Eine Geb�hrenvorlage ist ein Python-Skript, welches von FEAS bei einer Buchung herangezogen wird, um den zu bezahlenden Betrag zu berechnen. Die Variable, welche den zu buchenden Betrag an FEAS meldet, nennt sich einfach: charge. 

Au�erdem muss man wissen, dass alle Betr�ge als Flie�kommazahl �bertragen werden m�ssen, weshalb ein Betrag von z.B. 15,34 Euro in Form von 15.34 an FEAS �bergeben werden muss. Bereits mit diesem Wissen kann eine einfache Geb�hrenvorlage erstellt werden, die einen beliebigen Festbetrag (im folgenden Beispiel 3,50 Euro) bucht:

    ``charge = 3.50``

Nun ist aber oftmals nicht beabsichtigt, dass einfach nur Festbetr�ge gebucht werden. Im folgenden Beispiel behandeln wir den Fall, dass f�r ein Motorflugzeug 1,75 Euro pro Minute Flugzeit abgebucht werden. Hierf�r ist der Zugriff auf die Flugzeit notwendig, also kann die Buchung erst mit der Landung erfolgen (da beim Start ja noch keine Flugzeit vorliegt). Die Flugzeit ist in der Variable flight_time enthalten, also muss diese mit dem Betrag 1.75 multipliziert werden. In der Geb�hren-Vorlage sieht das Ganze dann so aus:

    ``charge = 1.75 * flight_time``

Wenden wir uns nun einem etwas anspruchsvolleren Beispiel zu. Angenommen ein Segelflugzeug startet mit einem Flugzeug-Schlepp, wobei die Geb�hren abh�ngig von der Schlepph�he berechnet werden sollen. F�r 500 Meter Schlepph�he wird ein Sockelbetrag von 20,- Euro angenommen, f�r alle weiteren 100 Meter sollen 5,- Euro zus�tzlich berechnet werden.

Zun�chst ben�tigen wir nat�rlich wieder die Variable der Schlepph�he. Sie lautet tow_altitude und gibt die bei der Landung des Schleppflugzeuges angegebene Schlepph�he an (falls bei der Landung eingetragen). Zudem muss nun eine Abfrage erfolgen, ob die Schlepph�he 500 Meter �berhaupt �berstiegen hat. Daf�r ben�tigen wir eine if-Anweisung mit der wir den Betrag der Schlepph�he ermitteln k�nnen. Hierf�r m�ssen wir wissen, dass Python durch Einr�ckung feststellt, ob eine Zeile noch zur vorangegangenen Anweisung geh�rt, oder nicht. Eine Einr�ckung hat bei Python stets 4 Leerzeichen zu betragen, der Tabulator ist dabei strikt zu meiden! Die L�sung unserer Aufgabe k�nnte so aussehen:

Beispiel::

    if tow_altitude <= 500:
       charge = 20.00
    else:
       charge = 20.00 + int((tow_altitude - 400) / 100) * 5.00

Was macht dieses Skript nun eigentlich? Zun�chst wird abgefragt, ob die Schlepph�he kleiner gleich 500 Meter ist. Wenn ja, dann werden 20,- Euro Geb�hren f�llig. Andernfalls wird eine andere Formel ausgef�hrt, die es etwas in sich hat. Zun�chst finden wir unseren Sockelbetrag von 20,- Euro wieder. 

Hinzu addiert wird eine Integer-Zahl (Ganzzahl, bei der die Nachkommastellen einfach abgeschnitten werden), bei der von der Schlepph�he zun�chst 400 Meter abgezogen werden. Der �brig bleibende Wert wird nun durch 100 Meter geteilt und die Nachkommastellen vom Zwischenergebnis einfach abgeschnitten. Dieses Zwischenergebnis muss nun nur noch mit dem Aufschlag pro 100 Meter multipliziert werden (in unserem Beispiel einfach 5,- Euro) und fertig ist die Formel.

Alle Variablen
Es existieren auch noch andere Variablen, die FEAS zur Berechnung von Geb�hren heranziehen kann. Auch k�nnen prinzipiell alle Operatoren verwendet werden, die Python 2.5 bietet! Da die Auff�hrung all dieser Operatoren den Rahmen dieser Anleitung sprengen w�rde, sei an dieser Stelle auf die Python 2.5-Dokumentation verwiesen. Trotzdem sind die wichtigsten Befehle in der folgenden Kurzreferenz aufgef�hrt, da man mit deren Hilfe schon fast alle existierenden Geb�hrenkonstrukte kreieren kann.

 * ``tow_altitude`` = Schlepph�he (Meter), welche bei der Landung in das Formular eingetragen wird, sofern der Flug mit der Startart "Flugzeug-Schlepp" gestartet wurde. 

 * ``motor_runtime`` = Motorlaufzeit (Minuten), wenn bei Start und Landung ein Z�hlerstand angegeben wird. 

 * ``flight_time`` = Zeit (Minuten), die zwischen Start und Landung vergangen ist. 

 * ``charge`` = Betrag, der entweder bei Start oder Landung gebucht wird (abh�ngig davon, ob es sich um eine Vorlage in der Start- oder Lande-Geb�hren-Tabelle handelt). Diese Variable ist in jeder Geb�hren-Vorlage essentiell, da ohne sie keine Buchung stattfinden kann!  

Die wichtigsten Operatoren in Python sind:

 * ``==`` Ist gleich 

 * ``<`` kleiner 

 * ``>`` gr�sser

 * ``>=`` gr�sser gleich

 * ``<=`` kleiner gleich

 * ``<>`` ungleich 

Diese k�nnen in ``if``-, ``else``- oder ``elif``-Anweisungen verwendet werden, um Werte und Variablen miteinander zu vergleichen.

Um Variablen und Werte zu berechnen, werden folgende Operatoren verwendet:

 * ``x + y`` x plus y (addieren)

 * ``x - y`` y minus x (subtrahieren)

 * ``x * y`` x mal y (multiplizieren)

 * ``x / y`` x durch y (dividieren)

 * ``x % y`` x modulo y (Rest einer Division, z.B. ``17 % 3`` = 2) 

 * ``x ** y`` x hoch y (z.B. ``4**2`` = 16)

Die wichtigsten Typumwandlungs-Operatoren sind:

 * ``int(x)`` Integer = Ganzzahl, abschneiden der Nachkommastellen, z.B. ``4``

 * ``float(x)`` Float = Flie�kommazahl, z.B. ``5.43`` 

