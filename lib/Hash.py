import hashlib


def hashing(filename):

    hash = hashlib.md5()

    with open(filename, 'rb') as file:
        buffer = file.read()
        hash.update(buffer)
    return hash.hexdigest()


value = hashing("Voer hier het pad in")
print("De MD5-Hash:", value)

