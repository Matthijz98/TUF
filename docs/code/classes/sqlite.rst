######
SQLite
######

******
SQLite
******
De Sqlite classe can worden gebruik om verbinding te maken met de Sqlite database.


Atributes
=========
- file
- path
- conn
- c

*********
\__init__
*********

Arguments
=========
:path: (string) path waar de database wordt opgeslagen
:filename: (string) bestands naam van het database bestand

Voordbeeld
==========
::

    Sqlite = new Sqlite('C:\Users\%username%\Documents', 'FUT-database')``

*******************
setUpDataBase(self)
*******************
De ``setUpDataBase(self)`` kan gebruikt worden om een database aan te maken en de tabel structuur op te zetten.

Arguments
=========
:Self: This arguments is provided by default

Voorbeeld
=========
::

    setUpDataBase()

*******************
checkDataBase(self)
*******************
De ``checkDataBase(self)`` is een functie om de database te controleren. De functie returnd een 0 als alles goed is. Of 1 als er iets niet goed is samen met een error bericht.

Argugemts
=========
:Self: This arguments is provided by default

Voordbeeld
==========
::

    if checkDatabase == 1:
        print error

************************
setLogItem(self, values)
************************
De ``setLogItem(self, values)`` fucntie kan worden gebruik om een logitem in de database op te slaan.

Arguments
=========
:Self: This arguments is provided by default
:values: array met (int)evidence_id, (int)session_id, (int)case_id, (String)date_time, (String)title, (String)details

