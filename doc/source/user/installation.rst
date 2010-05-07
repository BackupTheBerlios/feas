.. _Installation:

Installation
============
.. topic:: Zusammenfassung

   Hier wird gezeigt, wie FEAS installiert wird.
   
Eine FEAS-Installation besteht aus zwei Teilen. Der erste Teil ist das Programm FEAS selbst, der zweite Teil ist eine SQL-Datenbank.


Datenbank
---------
Da FEAS auf einer SQL-Datenbank basiert muss diese bereits vorhanden sein, wenn FEAS zum ersten mal gestartet wird. 

.. note:: FEAS kann nicht nur auf eine lokal installierte Datenbank zugreifen, sondern auch auf Datenbanken, die auf entfernten Rechnern (z.B. im Internet) installiert sind. Hier wird der Einfachheit halber nur auf die lokale installation der Datenbank eingegangen.

FEAS wurde auf Basis der freien PostgreSQL-Datenbank entwickelt, welche im Internet zum Download bereitsteht. 

Nachdem das Paket `PostgreSQL` heruntergeladen wurde, ist es zunächst einmal zu entpacken. Danach muss das Installationspaket ``postgresql-8.2`` gestartet werden, welches auch gleich nach der zu installierenden Sprache fragen sollte. Wir wählen standesgemäß `German / Deutsch` aus, und fahren mit dem Button `Start >` fort.

Danach empfiehlt der PostgreSQL-Installer, `alle Windows-Anwendungen zu beenden`, was wir natürlich befolgen sollten um anschließend mit dem Button `Weiter >` fortzufahren. Daraufhin erscheint ein Fenster mit `Installationshinweisen`, die wir wieder mit dem Button `Weiter >` quittieren. Dann erscheint ein weiterer Dialog mit `Installationsoptionen`, welchen wir ebenfalls mit dem Button `Weiter >` überblättern.

Nun befinden wir uns in der `Dienste-Konfiguration`. Hier ist ein Kennwort zu vergeben, das man sich merken sollte. Es ist für die spätere Einrichtung der FEAS-Datenbank erforderlich. Alle anderen Felder sollten bereits automatisch korrekt ausgefüllt sein. Wenn das Kennwort vergeben uns bestätigt wurde, quittieren wir den Dialog wieder mit dem Button `Weiter >`. Daraufhin fragt der Installer, ob das nicht gefundene Benutzerkonto angelegt werden soll, was mit dem Button `Ja` zu quittieren ist. Eventuell folgt ein Dialog, in dem gefragt wird, ob das `scheinbar leicht erratbare Kennwort` durch ein `schwer zu erratendes` ersetzt werden soll. Dies kann mit dem Button `Nein` quittiert werden, wenn man das vergebene Kennwort für gut genug hält. Andernfalls legt der Installer automatisch ein Kennwort an, was wirklich kaum zu erraten ist und deshalb auch unbedingt notiert werden müsste!

Nach diesem Dialog folgt der Dialog `Datenbank-Cluster initialisieren`. Hier sollte im Feld `Encoding` unbedingt die Option `LATIN1` ausgewählt werden. Im Feld `Kennwort` ist das im letzten Dialog vergebene Kennwort einzugeben und im nächsten Feld zu bestätigen. Sind diese Eingaben getätigt, quittieren wir den Dialog wieder mit dem Button `Weiter >`.

Nun Folgt der Dialog `Prozedurale Sprachen aktivieren`. Hier stimmen wieder alle Einstellungen, deshalb drücken wir wieder den Button `Weiter >`.

Ebenso verfahren wir im Dialog `Aktiviere Contrib-Module`. Auch hier sind alle Einstellungen richtig, deshalb wieder `Weiter >`. Am Ende erscheint der Dialog `Bereit zum Installieren`, was ebenfalls wieder durch den Button `Weiter >` bestätigt wird.

Nun startet endlich die Installation der Datenbank...

Nach erfolgter Installation folgt der Dialog `Installation vollständig!`, was einfach mit dem Button `Beenden` bestätigt werden kann. Nun sollte die PostgreSQL-Datenbank installiert sein, womit der FEAS-Installation nichts mehr im Wege steht!


FEAS
----
Unter Windows ist FEAS einfach zu installieren, da ein Installationspaket zur Verfügung steht.

Die Installation von FEAS startet mit einem Doppelklick auf den zuvor heruntergeladenen Installer. Zunächst öffnet sich der Dialog `Lizenzabkommen`. Dieses ist mit dem Button `Annehmen` zu quittieren, damit die Installation fortgesetzt wird.

Es folgt der Dialog `Zielverzeichnis auswählen`, womit das Installationsverzeichnis von FEAS gemeint ist. Normalerweise kann dieser Dialog einfach mit dem Button `Installieren` quittiert werden, da der Installer automatisch das Programme-Verzeichnis von Windows gewählt hat.

Nun folgt die Installation von FEAS...

Ist die Installation fertiggestellt, erscheint der Dialog `Die Installation ist vollständig`. Dies kann wieder mit dem Button `Beenden` quittiert werden, womit sich das Installationsprogramm beenden sollte. Wenn alles glatt gelaufen ist, dann kann FEAS nun zum ersten mal gestartet werden. Dies wird im nächsten Kapitel :ref:`erste_Schritte` näher beschrieben.


