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
# requestst importeren voor het versturen van het bestand
import requests


# klasse VirusTotal aanmaken voor
class VirusTotal:
    # Hier wordt de key meegegeven
    api = '576218e742aa0a0470bcc4a59146b58ab585d44cc36a84fd837594ec8005bed6'

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


    def upload_file(self, filename):
        params = {'apikey': self.api}
        files = {'file': ('',
                          open(filename, 'rb'))}

        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        print(response)
        json_response = response.json()
        print("VirusTotal geeft het volgende terug:", json_response, "\n")
        return json_response

    def test_file(self, filename):
        # hash to file
        filehash = self.hashFile(filename)
        # get the reponse of the hash upload
        response_hash = self.send_hash(filehash)
        print("response: ", response_hash)
        # check if the result reponse code is 0
        if response_hash['results']['response_code'] == 0:
            # if reponse is 0 upload the hole file and return the response
            return self.report(self.upload_file())
        else:
            # if the hash is working just return that
            return self.report(response_hash)


if __name__ == '__main__':
    vt = VirusTotal('')
    testfile = "C:/Users/mzond/OneDrive/Downloads/header-server.png"
    print(vt.hashFile(testfile))
    print(vt.send_hash(vt.hashFile(testfile)))
    print(vt.upload_file(testfile))
    print(vt.test_file(testfile))

