.. _Zusammenfassung:

===============
Zusammenfassung
===============
.. topic:: Zusammenfassung

Werkzeuge
---------

FEAS wurde in der Programmiersprache Python verfasst. Es greift auf eine SQL-Datenbank zu, in der nahezu alle Daten gespeichert werden. Da FEAS ein open source Projekt ist, wurde der gesamte Quellcode über das Internet verfügbar gemacht. Folgende Auflistung gibt einen Überblick der verwendeten Entwicklungs-Tools.

 * Python - Mit dieser Programmiersprache wurde FEAS verfasst.
 * EasyEclipse for Python - Mit dieser Entwicklungsumgebung wurde fast der gesamte Quellcode für FEAS erstellt.
 * GTK+ - Die grafische Benutzeroberfläche für nahezu alle Plattformen.
 * GLADE - Grosse Teile der FEAS-Benutzeroberfläche wurden mit dem bei GTK+ mitgelieferten GUI-Editor "GLADE" gezeichnet.
 * NSIS - Die Installationsroutine von FEAS wurde mit diesem Installer-Toolkit entworfen.
 * TortoiseSVN - Wird zur Versionskontrolle von FEAS verwendet.


Datenbankaufbau
---------------
- Als Datenbank fuer FEAS dient PostgreSQL. Die Verbindung erfolgt ueber PyGreSQL, einem Python-Modul, welches die Ankopplung der PostgreSQL-Datenbank sicherstellt. Im Folgenden werden nun die zusammenhaenge innerhalb der FEAS-Datenbank erlaeutert, um einen ueberblick ueber die Tabellen und deren Verknüpfungen zu erhalten.

Überlegungen
------------
Die Tabellen ``aircraft`` und ``flight_types`` sind eigenstaendig. Die Aufgabenstellung lautet, jedem Flugzeug (entspricht einer Zeile in der ``aircraft``-Tabelle) die erlaubten ``flight_types`` (jeder flight_type entspricht ebenfalls einer Zeile in der ``flight_types``-Tabelle) zuweisen zu können. Dabei muessen jedem einzelnen Flugzeug alle flight_types zur Auswahl stehen!
Wie könnte man das am besten lösen?

Installer fuer FEAS
-------------------
Das Problem besteht darin, eine plattformübergreifend funktionierende Installationsroutine fuer FEAS zu schaffen. Zunaechst soll Windows in Augenschein genommen werden, trotzdem muss ueber den Tellerrand geschaut werden, um sich die Erstellung einer Installationsroutine fuer Linux nicht zu verbauen oder zu erschweren.
Das Build-Tool sollte schon mal für Windows und Linux verfuegbar sein. CX-Freeze sollte diese Arbeit erstmal befriedigend bewerkstelligen. Bleibt noch zu ueberlegen, wie man es am besten einbindet, um die reinen Binaries zu erstellen. Unter Windows wurde bereits ein erfolgreicher Versuch gestartet, Linux ist noch außen vor. Das soll aber auch noch eine Weile so bleiben, denn Linux ist erstmal nicht ganz so wichtig - mein Aeroclub benutzt ja derzeit nur Windows-Rechner!
Anschließend muessen die Binaries dann mit Hilfe eines Installers in ein Installationspaket verwandelt werden. Hier endet die Plattform uebergreifende Auslegung der Tools, da man unter Linux kaum NSIS oder aehnliches verwenden kann. Fuer Linux sollten RPM-Pakete erstellt werden, sofern dies moeglich ist.
Zum Komplettpaket gehoeren GTK+ Runtime, PostgreSQL 8.4 und eben die FEAS Binaries. Den build zu erstellen sollte mit einem Knopfdruck moeglich werden, genau wie das Paket an sich... 

Filebundle für Datenbank-Tabelle
--------------------------------
- gladefile mit:
  - portlet
  - formular
- tabellendefinition.py
- report-definitionen

Hauptfile
---------
- table_portlet.py

Es muss noch moeglich werden, die Tabellen-Spalten mit Werten auszufuellen, die von einer anderen Tabelle aus mit einer Spalte aus der Haupttabelle verknüpft sind!

