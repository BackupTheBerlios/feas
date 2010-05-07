.. _Entwicklungstagebuch:

====================
Entwicklungstagebuch
====================
.. topic:: Entwicklungstagebuch

   Das Tagebuch eben, ahnlich einem Blog.
      
   
21. Dezember 2009
=================
Jetzt ist es wieder mal so weit. Es wird wie immer ein Report-Modul benötigt, das schwierig zu erschaffen ist. Mal sehen, was diesmal dabei rumkommt. Zunächst sollte es eine einfache Seitenbeschreibungssprache geben. Diese fängt sinnigerweise mit folgendem tag an:
Reportlab ist zwar nicht schlecht, hat aber ein eigenes Selbstverständnis!

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
   Man könnte es sich einigermaßen einfach machen, wenn man das ``Form`` einfach als
   Gruppe definiert, die alle Primitives enthalten kann. Es werden soviele davon
   hintereinander auf eine ``Page`` gedruckt, bis diese voll ist. Anschließend wird
   einfach auf der 0-Koordinate der ``Page`` wieder angefangen.
 

11. November 2009
=================
Zumindest das Hauptprogramm lässt sich jetzt wieder einigermassen Reibungslos aufrufen. Die Menütabelle funktioniert wieder, wenn auch die hinterlegten Portlets noch nicht funktionieren. Die Formulare wurden zumindest in der ``.glade``-Datei angepasst, so dass diese nun nicht mehr mit einer eigenen Toolbar kommen. Jedes Formular hat die gleiche (oder zumindest sehr ähnliche) Toolbar, weshalb selbige lieber in einer eigenen Formularklasse definiert werden sollte. Auch das berüchtigte ``table_portlet`` erhält nun seine widgets nicht mehr aus einer ``.glade``-Datei, es enthält ja ohnehin nur ``gtk.STOCK``-Buttons und eine ``gtk.TreeView``.

Jetzt ist die große Aufgabe, zunächst mal das ``person``-Portlet zur Funktion zu führen. Dafür müssen die Klassen ``Portlets.Table`` und ``Portlets.Form`` erst aus der Asche des alten ``table_portlet``-Moduls erschaffen werden. Dafür ist dann aber auch fast die komplette funktionalität aller übergreifenden Klassen und Methoden von FEAS in einem Framework verankert, das später auch für andere Applikationen herangezogen werden kann. Auch FEAS profitiert, weil neue Funktionen nun viel einfacher einzufügen sein werden.

Die Klassen ``Portlets.Form`` und ``Portlets.Table`` benötigen noch Methoden, um Fremdschlüssel einbinden zu können. Bei der ``Table``-Klasse aus dem Modul ``GTK`` heißt das, es müssten Comboboxentrys möglich sein, die man aus den Inhalten fremder Tabellen befülllen kann. Bei 1:1 Beziehungen kann ja eine Spalte eingebunden werden, deren ``column_name`` auf ein Feld der Fremdtabelle verweist. Es liegt dann nur noch am vorhanden sein der Eintrages im ``content_lod``. 

Beim Form verhält es sich ähnlich, man kann ja eine Tabelle auch als Formularsammlung sehen. Beide Klassen- ob ``Form`` oder ``Table`` haben dennoch das Problem, dass man - besonders beim ``Form``, ja auch die in den Fremdtabellen geänderten Werte schreiben muss. Das wurde bei FEAS mit einer ``portlet_list`` bewerkstelligt - was nicht sehr Pythonian ist. Ein ``list_of_dictionarys`` wäre da schon wesentlich ratsamer, weil man dann jederzeit Erweiterungen einfügen kann.

Das befüllen des Forms mit Daten aus fremden Tabellen ist bei 1:1 Beziehung - wie bei der ``Table`` - wieder nur eine Frage des vorhandenseins im ``content_lod``. Das bringt aber bei einem Form leider nichts, da die ``gtk.ComboBoxEntry`` ja irgendwie befüllt werden müssen. Man sollte in Erwägung ziehen, eine SQL-Abfrage für das befüllen jeder einzelnen ``gtk.ComboBoxEntry`` in einem ``portlets_lod`` zu statuieren. Dann ist nur wieder das speichern ein Problem !?

11. Dezember 2009
=================
Flugzeug hat:
 - Gebührenvorlage
 - erlaubte Startarten
 - erlaubte Landearten
 - erlaubte Flugarten
    
Gebührenvorlage hat:
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
FEAS wird nun zum dritten mal neu geschrieben. Es müssen letztenendes alle Erkenntnisse in das Framework einfließen!

 * Entwurf einer besseren ``ComboBoxEntry``.
 
 * Fertigstellung des Login.
 

31. Oktober 2009
================
Das komplette Framework wird nun in einen neuen Level übergehen. Die drei einzelnen Module :mod:`GTKapi`, :mod:`DBapi` und :mod:`Commons` werden in einem neuen Framework namens :mod:`dbGUIapi` vereinigt. Damit ist das Problem der schwindenden Modularität gebannt - mit allen Vorteilen für die Weiterentwicklung des Frameworks. Nun kann das Datenbankportlet aus einem übergeordneten Modul ``Portlets`` aufgerufen werden, welches alle Module der drei einzelnen Frameworks importieren kann. 

 * Die drei einzelnen Projekte bei BerliOS müssen gelöscht werden.
 
 * Ein neues Projekt Namens ``dbGUIapi`` muss erstellt werden.
 
 * Datenbankerkennung...

