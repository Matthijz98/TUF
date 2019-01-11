from virus_total_apis import PublicApi
import json
import hashlib


def hashing(filename):

    hash = hashlib.sha1()

    with open(filename, 'rb') as file:
        buffer = file.read()
        hash.update(buffer)
    return hash.hexdigest()


value = hashing("")
print("De sha1-hash:", value)


def send_hash(hash):
    key = ''

    api = PublicApi(key)

    response = api.get_file_report(hash)
    report(response)


def report(response):
    # string genereren
    dump = json.dumps(response)
    # object maken
    result = json.loads(dump)

    print(json.dumps(result, indent=4, sort_keys=True))

    results = result['results']

    if results is []:
        return False
    scans = results['scans']

    for item in scans.items():
        for detect, output in scans.items():
            #print(output.get('detected'))
            if output is 'True':
                print(output)
                break


if __name__ == '__main__':
    send_hash(value)
