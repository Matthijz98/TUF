"""
Gemaakt door:
Studentnummer: 
"""

# De publicApi importeren van virustotal
from virus_total_apis import PublicApi
# json library importeren voor het rapport van virustotal
import json
# hashlib importeren om eerst een hash waarde te berekenen voor virustotal
import hashlib
# requests importeren voor het versturen van het bestand
import requests

# imports voor de GUI
import PySimpleGUI as Sg


# klasse VirusTotal aanmaken
class VirusTotal:
    # Hier wordt de key meegegeven
    api = 'api_key meegeven'

    # Hier wordt de key aangeroepen
    # Met self zijn attributen en methoden toegankelijk in de klasse
    # init is de constructor. Als er een object wordt aangemaakt van de klasse
    # wordt dit aangeroepen voor het initialiseren van de attributen
    def __init__(self, api):
        self.api = api

    # Hiermee wordt een hashwaarde van het bestand berekent
    def hash_file(self, filename):

        # buffer size instellen zodat grotere bestanden sneller worden gelezen
        buffer_size = 65536
        # sha256 hash ophalen uit de library
        hash = hashlib.sha256()

        try:
            # bestand openen
            with open(filename, 'rb') as file:
                while True:
                    # bestand wordt gelezen met de meegegeven buffer_size
                    buffer = file.read(buffer_size)
                    # als de buffer leeg is dan stopt de while loop
                    if not buffer:
                        break
                    hash.update(buffer)
            # hash waarde wordt terugeggeven
            return hash.hexdigest()
        # een foutmelding terugggeven als er iets fout gaat met het openen of als het bestand niet bestaat
        except IOError:
            print("Er gaat iets fout met het lezen van het bestand.")

    # Met deze functie wordt de hashwaarde verstuurt naar VirusTotal
    def send_hash(self, filehash):
        # De PublicApi wordt doorgegeven aan api
        api = PublicApi(self.api)

        # response terugvragen van virustotal
        response = api.get_file_report(filehash)
        return response

    # hier wordt het rapport opgehaald als er een bestand wordt geüpload
    def get_report(self, resource):

        # api key en hash meegeven
        params = {'apikey': self.api, 'resource': resource}

        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
                                params=params)
        json_response = response.json()

        return json_response

    # hier wordt het bestand geupload naar virustotal
    def upload_file(self, filename):
        # api key meegeven
        params = {'apikey': self.api}

        # bestandslocatie meegeven
        files = {'file': (filename,
                          open(filename, 'rb'))}

        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)

        json_response = response.json()
        # de permalink wordt geprint, hiermee kan het rapport worden geopend
        return json_response['permalink']

    # hier wordt het bestand daadwerkelijk geupload als de hash niet wordt herkend
    def test_file(self, filename):
        # hash toekennen aan filehash
        filehash = self.hash_file(filename)

        # verkrijgen van response van de hash upload
        response_hash = self.send_hash(filehash)

        # kijken of de hashwaarde wordt herkend door VirusTotal
        if response_hash['results']['response_code'] == 0:

            # als de response code 0 is, dan wordt het hele bestand geupload
            Sg.Popup(f"{response_hash['results']['verbose_msg']}.\n\nThe file is now being uploaded.",
                     button_color=('black', 'yellow'))

            file_upload = self.upload_file(filename)
            return self.get_report(file_upload)

        # als de gebruiker nog een keer het bestand upload,
        # wordt er een melding teruggegeven dat het bestand in de wachtrij staat
        if response_hash['results']['response_code'] == -2:

            Sg.Popup(f"{response_hash['results']['verbose_msg']}.",
                     button_color=('black', 'yellow'))

        else:

            # als de hash wel werkt of als het bestand succesvol is gescand wordt dit terugegeven
            Sg.Popup(f"Positives: {response_hash['results']['positives']}", button_color=('black', 'yellow'))

            return response_hash


# main uitvoeren
if __name__ == '__main__':
    # api key meegeven
    # klasse aanmaken van VirusTotal
    vt = VirusTotal('api key')

    # bestand selecteren
    testfile = "bestandspad"

    # functie test_file uitvoeren
    vt.test_file(testfile)
