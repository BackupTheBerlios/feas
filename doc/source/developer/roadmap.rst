.. _Roadmap:

=======
Roadmap
=======
.. topic:: Roadmap

   Hier werden die geplanten Features der kommenden FEAS-Versionen angekündigt und alle bekannten Fehler aufgenommen.
   
Version 0.7
===========
Diese Version wird die erste stabile Produktiv-Version sein. Einige Mängel sind aber bis zum Release noch zu beheben, zudem müssen noch dringend einige Features hinzugefügt werden.

Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` fließen bereits in dieser Version mit ein, werden aber nur für die neuen Features verwendet. Alte Features werden noch mit den alt hergebrachten FEAS-Komponenten bewerkstelligt.

ToDo
----
 * Funktionierendes Abrechnungssystem
    * Bei landendem Schleppflugzeug ist die Schlepphöhe des Seglers einzutragen!
    * Die Landung funktioniert nicht mehr korrekt. Warum?
 * DFS-Direktiven (Meldepflicht bei Luftraumüberwachung) 
 * Funktionierende HTML-Reports
 * Geo-Koordinaten in den Einstellungen verfügbar machen, um Sunrise/Sunset genauer berechnen zu können!
 
Fertig
------
 * Dokumentation auf Sphinx umschwenken, damit HTML-Doku und PDF-Doku aus der selben Quelle erstellt werden können
 * Sunrise/Sunset berechnen
 

Version 0.8
===========
Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` sollen alte Code-Relikte vollständig ersetzen. Damit wird der Code flexibler und lesbarer, der Datenbankzugriff wird nicht mehr auf PostgreSQL beschränkt sein und viele Dateiformate wie z.B. ``csv`` und ``xls`` können unterstützt werden, um Datenexporte zu erstellen.

ToDo
----
 * Die Python-Module ``GTKapi``, ``DBapi`` und ``PyCommons`` müssen erst auf einen Stand gebracht werden, um für FEAS überhaupt nutzbar zu sein.