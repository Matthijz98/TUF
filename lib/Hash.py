"""
Gemaakt door:
Studentnummer:
"""

# Hash library importeren
import hashlib


# klasse Hashing maken
class Hashing:

    # constructor aanmaken
    def __init__(self):
        self

    # Functie hashing aanmaken met een parameter voor het bestand
    def hashing(filename):

        # buffer size instellen zodat grotere bestanden sneller worden gelezen
        buffer_size = 65536
        # sha1 hash ophalen uit de hashlib library
        hash = hashlib.sha1()

        try:
            # bestand openen
            with open(filename, 'rb') as file:
                while True:
                    # bestand wordt gelezen met de meegegeven buffer_size (65536)
                    buffer = file.read(buffer_size)
                    # als de buffer leeg is dan stopt de while loop
                    if not buffer:
                        break
                    # de hash wordt geupdate aan de hand van de buffer
                    hash.update(buffer)
            # hashwaarde wordt terugeggeven
            return hash.hexdigest()
        # een foutmelding terugggeven als er iets fout gaat met het openen of als het bestand niet bestaat
        except IOError:
            # foutmelding printen op het scherm
            print("Er gaat iets fout met het lezen van het bestand.")


# hashing functie uitvoeren
if __name__ == '__main__':
    # klasse aanmaken van Hashing
    hash_bestand = Hashing

    # file path meegeven aan de variabele value
    value = hash_bestand.hashing("bestand path invullen")
    # de hash printen
    print("De sha1-hash:", value)
