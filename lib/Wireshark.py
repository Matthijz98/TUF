"""
Gemaakt door:
Studentnummer:
"""

# Van de library scapy rdpcap en scapy_exception importeren
from scapy.all import rdpcap, Scapy_Exception
import os.path


# klasse Wrieshark aanmaken
class Wireshark:

    # constructor aanmaken
    def __init__(self):
        self

    # main functie aanmaken
    def main(self, filename):
        # het bestand splitsen om de extensie te checken
        name, ext = os.path.splitext(filename)

        # als het een .pcap extensie heeft moet de code uitgevoerd worden
        if ext == '.pcap':
            # Een try om te kijken of het wel een wireshark bestand is
            try:
                # rdpcap importeren van scapy. Dit laadt de file in.
                # hier wordt ook het bestand meegegeven
                packets = rdpcap(filename)

                # Hier worden het aantal packets getoond
                print("Aantal packets:", len(packets))

                # Hier wordt elke packet getoond
                for packet in packets:
                    packets.show()
                    break

            # Dit vangt de error op om vervolgens een melding terug te geven
            except Scapy_Exception:
                # hier wordt er een foutmelding getoond
                print("Dit is geen Wireshark bestand.")
            # Als het bestand niet bestaat ook een foutmelding teruggeven
            except FileNotFoundError:
                # hier wordt er een foutmelding getoond
                print("Dit is geen Wireshark bestand.")

        # Als het niet de extensie .pcap heeft wordt er een melding teruggegeven
        else:
            print("Dit is geen Wireshark bestand.")


# main uitvoeren
if __name__ == '__main__':
    # klasse aanmaken van Wireshark
    print_wireshark = Wireshark()

    # hier wordt de functie aangeroepen uit de klasse met de constructor
    print_wireshark.main("bestandspad invoeren")
