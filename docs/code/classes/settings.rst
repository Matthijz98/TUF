#########
Settings
#########
De settings classe kan gebruikt worden om settings uit het settings bestand te laden. En settings te bewaren voor later gebruik

********************
makeDefaultConfig()
********************
De ``makeDefaultConfig()`` functie maakt het config bestand en vult deze met de default waarde.

Arguments
==========
none

Voorbeeld
=========
::

    >> makeDefaultConfig():

**************
getSettings()
**************
De ``getSettings()`` functie returnt een array met daarin alle settings.

Arguments
=========
none

Voorbeeld
=========
::

    print(getSettings())
    >> {'fileName': 'database.db', 'filePatch': ''}

setSetting()
------------
De ``setSetting(section, key, value)`` functie kan worden gebruik om een setting aan te passen en op te slaan in het settings bestand.

Arguments
==========
:section: het gedeelte van het settings bestand waar de setting staat
:key: de key van de waarde die aangepast moet worden
:value: de nieuwe waarde van de setting

Voorbeeld
=========
::

    print(getSettings())
    >> {'fileName': 'database.db', 'filePatch': ''}

    setSetting('SQLite', 'filename', 'newfilename.db')

    print(getSettings())
    >> {'fileName': 'newfilename.db', 'filePatch': ''}



