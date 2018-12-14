############
Documentatie
############
De docuementatie van  het project is super belangrijk om te zorgen dat iedereen het snapt

****************************
Nieuwe documentatie aanmaken
****************************
Om de documentatie te kunnen maken en lokaal te testen heb je Sphinx nodig. Hoe dit geinstaleerd kan worden staat in de setup documentatie.
Het aanmaken van documentatie van een functie kan gewoon om de branch waar de functie zelf gemaakt wordt. Die later via een pull request op de master branch komt.

Nieuw document aanmaken
=======================
- Maak in de goede folder een nieuw document met een goede naam en ``.rst`` als de extentie
- Voeg dit bestand to aan je git

Document structuur
==================
Een handleiding document wordt gemaakt met een progemeer taal reStructuredText. Hier onder staan een aantal van de meest voorkomde codes

Headings

Lijsten

Code

Documentatie genereren
======================
- Open een terminal en type ``make html``
- Open de index.html in de docs/_build folder
- Check of de pagina klopt en de menu structuur in de zijbalk
