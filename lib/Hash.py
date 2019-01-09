import hashlib


def hashing(filename):

    # buffer size instellen zodat grotere bestanden sneller worden gelezen
    buffer_size = 65536
    hash = hashlib.md5()

    # bestand openen
    with open(filename, 'rb') as file:
        while True:
            buffer = file.read(buffer_size)
            if not buffer:
                break
            hash.update(buffer)
    return hash.hexdigest()


# file path aangeven en de md5 printen
value = hashing("")
print("De MD5-Hash:", value)

