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
    api = ''

    # Hier wordt de key aangeroepen
    def __init__(self, api):
        self.api = api

    # Hiermee wordt een hashwaarde van het bestand berekent
    def hashFile(self, filename, buffer_size=65536):
        try:
            file = open(filename, 'rb')
        except IOError:
            return None
        except:
            return None
        hashing = hashlib.sha1()
        buffer = file.read(buffer_size)
        while len(buffer) > 0:
            hashing.update(buffer)
            buffer = file.read(buffer_size)
        file.close()
        return hashing.hexdigest()

    # Met deze functie wordt de hashwaarde verstuurd naar VirusTotal
    def send_hash(self, hashing):
        # De PublicApi wordt doorgegeven aan api
        api = PublicApi(self.api)

        response = api.get_file_report(hashing)
        self.report(response)

    # Hier wordt het rapport opgevraagd van VirusTotal
    def report(self, response):
        # string genereren
        dump = json.dumps(response)
        # object maken
        result = json.loads(dump)

        # De json wordt netjes onder elkaar geprint
        print(json.dumps(result, indent=4, sort_keys=True))

        # Results van VirusTotal wordt doorgegeven aan results
        results = result['results']

        # Als VirusTotal de hashwaarde niet herkend, wordt dit uitgevoerd
        if results is []:
            if result['results']['response_code'] == 0:
                print('geen resulaten')

                params = {'apikey': 'api key invoeren'}
                files = {'file': ('path naar bestand',
                                  open('path naar bestand', 'rb'))}

                response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)

                json_response = response.json()
                print("VirusTotal geeft het volgende terug:", json_response, "\n")

            elif result['results']['response_code'] == 1:
                scans = results['scans']

                for item in scans.items():
                    for detect, output in scans.items():
                        # print(output.get('detected'))
                        if output is 'True':
                            print(output)
                            break
        return False


if __name__ == '__main__':
    vt = VirusTotal('api key invoeren')
    vt.send_hash(vt.hashFile(filename='path aangeven'))

