.. _Roadmap:

=======
Roadmap
=======
.. topic:: Roadmap

   Hier werden die geplanten Features der kommenden FEAS-Versionen angek�ndigt und alle bekannten Fehler aufgenommen.
   
Version 0.7
===========
Diese Version wird die erste stabile Produktiv-Version sein. Einige M�ngel sind aber bis zum Release noch zu beheben, zudem m�ssen noch dringend einige Features hinzugef�gt werden.

Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` flie�en bereits in dieser Version mit ein, werden aber nur f�r die neuen Features verwendet. Alte Features werden noch mit den alt hergebrachten FEAS-Komponenten bewerkstelligt.

ToDo
----
 * Funktionierendes Abrechnungssystem
    * Bei landendem Schleppflugzeug ist die Schlepph�he des Seglers einzutragen!
    * Die Landung funktioniert nicht mehr korrekt. Warum?
 * DFS-Direktiven (Meldepflicht bei Luftraum�berwachung) 
 * Funktionierende HTML-Reports
 * Geo-Koordinaten in den Einstellungen verf�gbar machen, um Sunrise/Sunset genauer berechnen zu k�nnen!
 
Fertig
------
 * Dokumentation auf Sphinx umschwenken, damit HTML-Doku und PDF-Doku aus der selben Quelle erstellt werden k�nnen
 * Sunrise/Sunset berechnen
 

Version 0.8
===========
Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` sollen alte Code-Relikte vollst�ndig ersetzen. Damit wird der Code flexibler und lesbarer, der Datenbankzugriff wird nicht mehr auf PostgreSQL beschr�nkt sein und viele Dateiformate wie z.B. ``csv`` und ``xls`` k�nnen unterst�tzt werden, um Datenexporte zu erstellen.

ToDo
----
 * Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` m�ssen erst auf einen Stand gebracht werden, um f�r FEAS �berhaupt nutzbar zu sein.