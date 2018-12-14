######
SQLite
######

De Sqlite classe can worden gebruik om verbinding te maken met de Sqlite database.

*********
Atributes
*********
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

***************
setUpDataBase()
***************
De ``setUpDataBase(self)`` functie kan gebruikt worden om een database aan te maken en de tabel structuur op te zetten.

Arguments
=========
:Self: This arguments is provided by default

Voorbeeld
=========
::

    setUpDataBase()

***************
checkDataBase()
***************
De ``checkDataBase(self)`` fucntie kan gebruikt worden om de database te controleren. De functie returnd een 0 als alles goed is. Of 1 als er iets niet goed is samen met een error bericht.

Argugemts
=========
:Self: This arguments is provided by default

Voordbeeld
==========
::

    if checkDatabase == 1:
        print error

************
setLogItem()
************
De ``setLogItem(self, values)`` fucntie kan worden gebruik om een logitem in de database op te slaan.

Arguments
=========
:self: This arguments is provided by default
:values: array met (int)evidence_id, (int)session_id, (int)case_id, (String)date_time, (String)title, (String)details

********************
getLogItemDetails()
********************
De ``getLogItemDetails(self, logId):`` fucntie kan gebruikt worden om alle details van logTiems te krijgen. De functie heeft een logId nodig om de goede log regel.

Arguguments
============
:self: This arguments is provided by default
:lodId: Het logId van de logregel waarvan meer je meer details wilt hebben

Voordbeeld
==========
::

    print getLodDetails(1)
    >> [evidence_id: '1', session_id: 1, case_id: '1',date_time:'141220180915' , title: 'this is a title',     >> [evidence_id: '1', session_id: 1, case_id: '1',date_time:'141220180915' , title: 'this is a title', details: 'This is some details about this log']

*************
getLogItems()
*************
De ``getLogItems(self, args):`` kan gebruikt worden om alle log items te vinden die aan specifieke voorwaarde voldoen.

Arguments
=========
:self: This arguments is provided by default
:args: Een lijst met argumenten waaraan de logitems moeten voldoen

Voorbeelden
===========
::

    args = "evidenceID='1'"
    print getLogItems(args)
    >> [[logId: 1, title: 'logtitle 1', dateTime: '141220180915'], [logId: 1, title: 'logtitle 1', dateTime: '161220181022']]

*********
setCase()
*********
De ``setCase(values)`` kan worden gebruikt om een case aantemaken in de database.

Arguments
=========
:self: This argument is provided by default
:values: Een array bestaande uit created_date text, title text, description text

Voorbeeld
=========
::

    values = [created_date:'141220180951' , title: 'The Case Title', description: 'The case description']
    setCase(values)

****************************
getCase(self, caseId, fields)