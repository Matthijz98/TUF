# Hash library importeren
import hashlib


# Functie hashing aanmaken met een parameter voor het bestand
def hashing(filename):

    # buffer size instellen zodat grotere bestanden sneller worden gelezen
    buffer_size = 65536
    # sha1 hash ophalen uit de library
    hash = hashlib.sha1()

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


# file path aangeven en de md5 printen
value = hashing(" ")
print("De sha1-hash:", value)

