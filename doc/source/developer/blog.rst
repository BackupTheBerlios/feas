.. _Entwicklungstagebuch:

====================
Entwicklungstagebuch
====================
.. topic:: Entwicklungstagebuch

   Das Tagebuch eben, ahnlich einem Blog.
      
   
21. Dezember 2009
=================
Jetzt ist es wieder mal so weit. Es wird wie immer ein Report-Modul ben�tigt, das schwierig zu erschaffen ist. Mal sehen, was diesmal dabei rumkommt. Zun�chst sollte es eine einfache Seitenbeschreibungssprache geben. Diese f�ngt sinnigerweise mit folgendem tag an:
Reportlab ist zwar nicht schlecht, hat aber ein eigenes Selbstverst�ndnis!

Die Seite selbst
----------------
 * ``Page`` - Die Seitendefinition.
 
Primitives
----------
 * ``Text`` - Ein beliebig definierbares Textfeld auf dem Blatt, immer an eine Position gebunden (so wie alles!).
 
 * ``Line`` - Eine Linie von a nach b, mehr nicht.
 
 * ``Image`` - Bild, egal ob im Vordergrund oder Hintergrund!

Gruppen
-------
 * ``Table`` - Eine Tabelle.
 
 * ``Form`` - Eine Subseite (Die Kreuzung aus ``Table`` und ``Page``.
   Man k�nnte es sich einigerma�en einfach machen, wenn man das ``Form`` einfach als
   Gruppe definiert, die alle Primitives enthalten kann. Es werden soviele davon
   hintereinander auf eine ``Page`` gedruckt, bis diese voll ist. Anschlie�end wird
   einfach auf der 0-Koordinate der ``Page`` wieder angefangen.
 

11. November 2009
=================
Zumindest das Hauptprogramm l�sst sich jetzt wieder einigermassen Reibungslos aufrufen. Die Men�tabelle funktioniert wieder, wenn auch die hinterlegten Portlets noch nicht funktionieren. Die Formulare wurden zumindest in der ``.glade``-Datei angepasst, so dass diese nun nicht mehr mit einer eigenen Toolbar kommen. Jedes Formular hat die gleiche (oder zumindest sehr �hnliche) Toolbar, weshalb selbige lieber in einer eigenen Formularklasse definiert werden sollte. Auch das ber�chtigte ``table_portlet`` erh�lt nun seine widgets nicht mehr aus einer ``.glade``-Datei, es enth�lt ja ohnehin nur ``gtk.STOCK``-Buttons und eine ``gtk.TreeView``.

Jetzt ist die gro�e Aufgabe, zun�chst mal das ``person``-Portlet zur Funktion zu f�hren. Daf�r m�ssen die Klassen ``Portlets.Table`` und ``Portlets.Form`` erst aus der Asche des alten ``table_portlet``-Moduls erschaffen werden. Daf�r ist dann aber auch fast die komplette funktionalit�t aller �bergreifenden Klassen und Methoden von FEAS in einem Framework verankert, das sp�ter auch f�r andere Applikationen herangezogen werden kann. Auch FEAS profitiert, weil neue Funktionen nun viel einfacher einzuf�gen sein werden.

Die Klassen ``Portlets.Form`` und ``Portlets.Table`` ben�tigen noch Methoden, um Fremdschl�ssel einbinden zu k�nnen. Bei der ``Table``-Klasse aus dem Modul ``GTK`` hei�t das, es m�ssten Comboboxentrys m�glich sein, die man aus den Inhalten fremder Tabellen bef�lllen kann. Bei 1:1 Beziehungen kann ja eine Spalte eingebunden werden, deren ``column_name`` auf ein Feld der Fremdtabelle verweist. Es liegt dann nur noch am vorhanden sein der Eintrages im ``content_lod``. 

Beim Form verh�lt es sich �hnlich, man kann ja eine Tabelle auch als Formularsammlung sehen. Beide Klassen- ob ``Form`` oder ``Table`` haben dennoch das Problem, dass man - besonders beim ``Form``, ja auch die in den Fremdtabellen ge�nderten Werte schreiben muss. Das wurde bei FEAS mit einer ``portlet_list`` bewerkstelligt - was nicht sehr Pythonian ist. Ein ``list_of_dictionarys`` w�re da schon wesentlich ratsamer, weil man dann jederzeit Erweiterungen einf�gen kann.

Das bef�llen des Forms mit Daten aus fremden Tabellen ist bei 1:1 Beziehung - wie bei der ``Table`` - wieder nur eine Frage des vorhandenseins im ``content_lod``. Das bringt aber bei einem Form leider nichts, da die ``gtk.ComboBoxEntry`` ja irgendwie bef�llt werden m�ssen. Man sollte in Erw�gung ziehen, eine SQL-Abfrage f�r das bef�llen jeder einzelnen ``gtk.ComboBoxEntry`` in einem ``portlets_lod`` zu statuieren. Dann ist nur wieder das speichern ein Problem !?

11. Dezember 2009
=================
Flugzeug hat:
 - Geb�hrenvorlage
 - erlaubte Startarten
 - erlaubte Landearten
 - erlaubte Flugarten
    
Geb�hrenvorlage hat:
 - Zuordnung

+----------------+-------+----------+-----+
| flart\strt.art | Wynch | Doub.tow | tow |
+================+=======+==========+=====+
| X              | c.tpl |   ...    |     |
+----------------+-------+----------+-----+
| F              |       |          |     |
+----------------+-------+----------+-----+
| B              |       |          |     |
+----------------+-------+----------+-----+
| A              |       |          |     |
+----------------+-------+----------+-----+
| L              |       |          |     |
+----------------+-------+----------+-----+


10. November 2009
=================
FEAS wird nun zum dritten mal neu geschrieben. Es m�ssen letztenendes alle Erkenntnisse in das Framework einflie�en!

 * Entwurf einer besseren ``ComboBoxEntry``.
 
 * Fertigstellung des Login.
 

31. Oktober 2009
================
Das komplette Framework wird nun in einen neuen Level �bergehen. Die drei einzelnen Module :mod:`GTKapi`, :mod:`DBapi` und :mod:`Commons` werden in einem neuen Framework namens :mod:`dbGUIapi` vereinigt. Damit ist das Problem der schwindenden Modularit�t gebannt - mit allen Vorteilen f�r die Weiterentwicklung des Frameworks. Nun kann das Datenbankportlet aus einem �bergeordneten Modul ``Portlets`` aufgerufen werden, welches alle Module der drei einzelnen Frameworks importieren kann. 

 * Die drei einzelnen Projekte bei BerliOS m�ssen gel�scht werden.
 
 * Ein neues Projekt Namens ``dbGUIapi`` muss erstellt werden.
 
 * Datenbankerkennung...

