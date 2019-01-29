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
# importeren timer
import time

import PySimpleGUI as Sg
import webbrowser


# klasse VirusTotal aanmaken voor
class VirusTotal:
    # Hier wordt de key meegegeven
    api = 'api key'

    # Hier wordt de key aangeroepen
    def __init__(self, api):
        self.api = api

    # Hiermee wordt een hashwaarde van het bestand berekent
    def hashFile(self, filename):

        # buffer size instellen zodat grotere bestanden sneller worden gelezen
        buffer_size = 65536
        # sha1 hash ophalen uit de library
        hash = hashlib.sha1()

        try:
            # bestand openen
            with open(filename, 'rb') as file:
                while True:
                    # bestand wordt gelezen met de meegegeven buffer_size
                    buffer = file.read(buffer_size)
                    if not buffer:
                        break
                    hash.update(buffer)
            # hash waarde wordt terugeggeven
            return hash.hexdigest()
        except IOError:
            print("Er gaat iets fout met het lezen van het bestand.")

    # Met deze functie wordt de hashwaarde verstuurd naar VirusTotal
    def send_hash(self, hashing):
        # De PublicApi wordt doorgegeven aan api
        api = PublicApi(self.api)

        response = api.get_file_report(hashing)
        return response

    def get_report(self, resource):
        #time.sleep(1)
        params = {'apikey': self.api, 'resource': resource}
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip,  My Python requests library example client or username"
        }
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
                                params=params, headers=headers)
        json_response = response.json()

        return json_response

    """"
    # Hier wordt het rapport opgevraagd van VirusTotal
    def print_report(self, response):
        # string genereren
        dump = json.dumps(response)
        # object maken
        result = json.loads(dump)

        # De json wordt netjes onder elkaar geprint
        print(json.dumps(result, indent=4, sort_keys=True))

        # Results van VirusTotal wordt doorgegeven aan results
        results = result['results']
    """

    def upload_file(self, filename):
        params = {'apikey': self.api}
        files = {'file': ('',
                          open(filename, 'rb'))}

        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        #print(response)
        json_response = response.json()
        return json_response['permalink']

    def test_file(self, filename):
        # hash to file
        filehash = self.hashFile(filename)
        # get the reponse of the hash upload
        response_hash = self.send_hash(filehash)
        # print("response: ", response_hash)
        # check if the result reponse code is 0
        if response_hash['results']['response_code'] == 0:
            # if reponse is 0 upload the hole file and return the response
            x = self.upload_file(testfile)
            return self.get_report(x['resource'])
        else:
            # if the hash is working just return that
            return response_hash


if __name__ == '__main__':
    vt = VirusTotal('api key')
    testfile = "file path"


    print("Open de link voor het rapport:", vt.upload_file(testfile))
    hashresource = vt.upload_file(testfile)

    Sg.Popup("Open de link voor het rapport:", vt.upload_file(testfile), button_color=('black', 'yellow'))
    webbrowser.open(vt.upload_file(testfile))

