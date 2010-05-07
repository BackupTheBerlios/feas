.. index::
   Gebühren
   
========
Gebühren
========
   
Die Gebührenabrechnung in FEAS stützt sich auf drei Säulen. Zunächst ist im Modul "Flugarten" festzulegen, wer mit der Gebühren-Buchung belastet werden soll. Im darauf aufbaünden Modul "Gebühren" kann nun festgelegt werden, unter welchen Umständen der unter "Flugarten" genannte Zahler belastet wird. 

Das Gebührenmodul selbst ist in zwei Tabellen unterteilt. Jeweils eine für Startgebühren und eine für Landegebühren. Der Unterschied beider Tabellen ist, dass die Buchung der Startgebühren beim Start erfolgt und die Buchung der Landegebühren bei der Landung.

Um alle Szenarien des Flugbetriebs erfassen zu können und um Doppelte Arbeit zu vermeiden verwendet FEAS Python-Skript vorlagen zur Definition der Gebühren. Dies erscheint Anfangs zwar etwas übertrieben zu sein, doch nur so ist die Abdeckung aller möglichen Gebühren-Szenarien möglich.

Die Tabellen Startgebühren und Landegebühren lesen sich wie folgt:
Es ist für jede Flugart eine Zeile vorhanden, sowie jeweils eine Spalte für die verschiedenen Start-Arten vorhanden ist. Die verfügbaren Startarten sind Eigenstart, Windenstart und Schleppstart.

Nun ist es möglich, für jede der verschiedenen Flug- und Startarten eine Python-Skriptvorlage zu vergeben. Entweder existiert bereits eine Vorlage (welche bereits für eine andere Flug-/Startart angelegt wurde), oder man muss eine neü Vorlage erstellen.

Um eine Vorlage zu erstellen sind Kenntnisse in der Skriptsprache Python von Vorteil, aber nicht unbedingt notwendig. Im Folgenden wird anhand von Beispielen gezeigt, wie man eigene Gebühren-Vorlagen erstellen kann und welche Möglichkeiten zur Anpassung bestehen.

Definition einer Gebührenvorlage
Eine Gebührenvorlage ist ein Python-Skript, welches von FEAS bei einer Buchung herangezogen wird, um den zu bezahlenden Betrag zu berechnen. Die Variable, welche den zu buchenden Betrag an FEAS meldet, nennt sich einfach: charge. 

Außerdem muss man wissen, dass alle Beträge als Fließkommazahl übertragen werden müssen, weshalb ein Betrag von z.B. 15,34 Euro in Form von 15.34 an FEAS übergeben werden muss. Bereits mit diesem Wissen kann eine einfache Gebührenvorlage erstellt werden, die einen beliebigen Festbetrag (im folgenden Beispiel 3,50 Euro) bucht:

    ``charge = 3.50``

Nun ist aber oftmals nicht beabsichtigt, dass einfach nur Festbeträge gebucht werden. Im folgenden Beispiel behandeln wir den Fall, dass für ein Motorflugzeug 1,75 Euro pro Minute Flugzeit abgebucht werden. Hierfür ist der Zugriff auf die Flugzeit notwendig, also kann die Buchung erst mit der Landung erfolgen (da beim Start ja noch keine Flugzeit vorliegt). Die Flugzeit ist in der Variable flight_time enthalten, also muss diese mit dem Betrag 1.75 multipliziert werden. In der Gebühren-Vorlage sieht das Ganze dann so aus:

    ``charge = 1.75 * flight_time``

Wenden wir uns nun einem etwas anspruchsvolleren Beispiel zu. Angenommen ein Segelflugzeug startet mit einem Flugzeug-Schlepp, wobei die Gebühren abhängig von der Schlepphöhe berechnet werden sollen. Für 500 Meter Schlepphöhe wird ein Sockelbetrag von 20,- Euro angenommen, für alle weiteren 100 Meter sollen 5,- Euro zusätzlich berechnet werden.

Zunächst benötigen wir natürlich wieder die Variable der Schlepphöhe. Sie lautet tow_altitude und gibt die bei der Landung des Schleppflugzeuges angegebene Schlepphöhe an (falls bei der Landung eingetragen). Zudem muss nun eine Abfrage erfolgen, ob die Schlepphöhe 500 Meter überhaupt überstiegen hat. Dafür benötigen wir eine if-Anweisung mit der wir den Betrag der Schlepphöhe ermitteln können. Hierfür müssen wir wissen, dass Python durch Einrückung feststellt, ob eine Zeile noch zur vorangegangenen Anweisung gehört, oder nicht. Eine Einrückung hat bei Python stets 4 Leerzeichen zu betragen, der Tabulator ist dabei strikt zu meiden! Die Lösung unserer Aufgabe könnte so aussehen:

Beispiel::

    if tow_altitude <= 500:
       charge = 20.00
    else:
       charge = 20.00 + int((tow_altitude - 400) / 100) * 5.00

Was macht dieses Skript nun eigentlich? Zunächst wird abgefragt, ob die Schlepphöhe kleiner gleich 500 Meter ist. Wenn ja, dann werden 20,- Euro Gebühren fällig. Andernfalls wird eine andere Formel ausgeführt, die es etwas in sich hat. Zunächst finden wir unseren Sockelbetrag von 20,- Euro wieder. 

Hinzu addiert wird eine Integer-Zahl (Ganzzahl, bei der die Nachkommastellen einfach abgeschnitten werden), bei der von der Schlepphöhe zunächst 400 Meter abgezogen werden. Der übrig bleibende Wert wird nun durch 100 Meter geteilt und die Nachkommastellen vom Zwischenergebnis einfach abgeschnitten. Dieses Zwischenergebnis muss nun nur noch mit dem Aufschlag pro 100 Meter multipliziert werden (in unserem Beispiel einfach 5,- Euro) und fertig ist die Formel.

Alle Variablen
Es existieren auch noch andere Variablen, die FEAS zur Berechnung von Gebühren heranziehen kann. Auch können prinzipiell alle Operatoren verwendet werden, die Python 2.5 bietet! Da die Aufführung all dieser Operatoren den Rahmen dieser Anleitung sprengen würde, sei an dieser Stelle auf die Python 2.5-Dokumentation verwiesen. Trotzdem sind die wichtigsten Befehle in der folgenden Kurzreferenz aufgeführt, da man mit deren Hilfe schon fast alle existierenden Gebührenkonstrukte kreieren kann.

 * ``tow_altitude`` = Schlepphöhe (Meter), welche bei der Landung in das Formular eingetragen wird, sofern der Flug mit der Startart "Flugzeug-Schlepp" gestartet wurde. 

 * ``motor_runtime`` = Motorlaufzeit (Minuten), wenn bei Start und Landung ein Zählerstand angegeben wird. 

 * ``flight_time`` = Zeit (Minuten), die zwischen Start und Landung vergangen ist. 

 * ``charge`` = Betrag, der entweder bei Start oder Landung gebucht wird (abhängig davon, ob es sich um eine Vorlage in der Start- oder Lande-Gebühren-Tabelle handelt). Diese Variable ist in jeder Gebühren-Vorlage essentiell, da ohne sie keine Buchung stattfinden kann!  

Die wichtigsten Operatoren in Python sind:

 * ``==`` Ist gleich 

 * ``<`` kleiner 

 * ``>`` grösser

 * ``>=`` grösser gleich

 * ``<=`` kleiner gleich

 * ``<>`` ungleich 

Diese können in ``if``-, ``else``- oder ``elif``-Anweisungen verwendet werden, um Werte und Variablen miteinander zu vergleichen.

Um Variablen und Werte zu berechnen, werden folgende Operatoren verwendet:

 * ``x + y`` x plus y (addieren)

 * ``x - y`` y minus x (subtrahieren)

 * ``x * y`` x mal y (multiplizieren)

 * ``x / y`` x durch y (dividieren)

 * ``x % y`` x modulo y (Rest einer Division, z.B. ``17 % 3`` = 2) 

 * ``x ** y`` x hoch y (z.B. ``4**2`` = 16)

Die wichtigsten Typumwandlungs-Operatoren sind:

 * ``int(x)`` Integer = Ganzzahl, abschneiden der Nachkommastellen, z.B. ``4``

 * ``float(x)`` Float = Fließkommazahl, z.B. ``5.43`` 

