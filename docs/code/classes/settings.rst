Settings
========
De settings classe kan gebruikt worden om setings uit het settings bestand te laden.

makeDefaultConfig()
-------------------
De ``makeDefaultConfig()`` functie maakt het config bestand en vult deze met de default waarde.
arguments: none

getSettings()
-------------
De ``getSettings()`` functie returnt een array met daarin alle settings.
arguments: none

setSetting()
------------
De ``setSetting(section, key, value)`` functie kan worden gebruik om een setting aan te passen en op te slaan in het settings bestand.
arguments:
* section: het gedeelte van het settings bestand waar de setting staat
* key: de key van de waarde die aangepast moet worden
* value: de nieuwe waarde van de setting