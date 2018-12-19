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
setup_database()
***************
De ``setup_database(self)`` functie kan gebruikt worden om een database aan te maken en de tabel structuur op te zetten.

Arguments
=========
:Self: This arguments is provided by default

Voorbeeld
=========
::

    setup_database()

***************
check_database()
***************
De ``check_database(self)`` fucntie kan gebruikt worden om de database te controleren. De functie returnd een 0 als alles goed is. Of 1 als er iets niet goed is samen met een error bericht.

Argugemts
=========
:Self: This arguments is provided by default

Voordbeeld
==========
::

    if check_database == 1:
        print error

************
set_log_item()
************
De ``set_log_item(self, values)`` fucntie kan worden gebruik om een logitem in de database op te slaan.

Arguments
=========
:self: This arguments is provided by default
:values: array met (int)evidence_id, (int)session_id, (int)case_id, (String)date_time, (String)title, (String)details

********************
get_log_item_details()
********************
De ``get_log_item_details(self, logId):`` fucntie kan gebruikt worden om alle details van logTiems te krijgen. De functie heeft een logId nodig om de goede log regel.

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
get_log_items()
*************
De ``get_log_items(self, args):`` kan gebruikt worden om alle log items te vinden die aan specifieke voorwaarde voldoen.

Arguments
=========
:self: This arguments is provided by default
:args: Een lijst met argumenten waaraan de logitems moeten voldoen

Voorbeelden
===========
::

    args = "evidence_id='1'"
    print get_log_items(args)
    >> [[logId: 1, title: 'logtitle 1', dateTime: '141220180915'], [logId: 1, title: 'logtitle 1', dateTime: '161220181022']]

*********
set_case()
*********
De ``set_case(values)`` kan worden gebruikt om een case aantemaken in de database.

Arguments
=========
:self: This argument is provided by default
:values: Een array bestaande uit created_date text, title text, description text

Voorbeeld
=========
::

    values = [created_date:'141220180951' , title: 'The Case Title', description: 'The case description']
    set_case(values)

*********
get_case()
*********
De ``get_case(self, caseId, fields)`` functie kan gebruikt worden om gegevens van een case te krijgen.

Arguments
=========
:self: This argument is provided by default
:caseId: De caseId waarvan je meer details wilt hebben
:fields: De velden die je terug wilt hebben

Voorbeeld
=========
::

    print get_case(1, 'all')
    >> [created_date:'141220180951' , title: 'The Case Title', description: 'The case description']

**********
get_cases()
**********
De ``get_cases(self, args)`` fucntie kan gebruikt worden om alle cases te krijgen die aan een aantal voorwaarde voldoen

Arguments
=========
:self: This argument is provided by default
:args: De argumenten waaraan de cases moeten voldoen

Voorbeeld
=========
::

    args = "user_id=1"
    print get_cases(args)
    >> [created_date:'141220180951' , title: 'The Case Title', description: 'The case description'], [created_date:'141220180951' , title: 'The Case Title', description: 'The case description']

*****************
set_evidence_item()
*****************
De ``set_evidence_item(self, values)`` fucntie kan gebruikt worden om een evidence item aan te maken in de database

Arguments
=========
:self: This argument is provided by default
:values: Een array met de volgede waarde case_id, title text

Voorbeeld
=========
::

    values = [caseId: 1, caseId: 1, evidence_id: 1, title: 'evidence Title']
    set_evidence_item(values)