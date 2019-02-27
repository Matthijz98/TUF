"""
Gemaakt door:
Studentnummer:
"""

# Van de library scapy rdpcap en scapy_exception importeren
from scapy.all import rdpcap, Scapy_Exception, ls, raw, hexdump
import os.path

# imports voor de GUI
import PySimpleGUI as Sg


# klasse Wrieshark aanmaken
class Wireshark:

    # constructor aanmaken
    def __init__(self):
        self

    # main functie aanmaken
    def wireshark(self, filename):
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
                Sg.Popup(f"Aantal packets: {len(packets)}", button_color=('black', 'yellow'))

                # Hier wordt elke packet getoond
                for packet in packets:
                    packets.show()
                    break

            # Dit vangt de error op om vervolgens een melding terug te geven
            except Scapy_Exception:
                # hier wordt er een foutmelding getoond
                Sg.Popup("Dit is geen Wireshark bestand.", button_color=('black', 'yellow'))
            # Als het bestand niet bestaat ook een foutmelding teruggeven
            except FileNotFoundError:
                # hier wordt er een foutmelding getoond
                Sg.Popup("Dit bestand bestaat niet.", button_color=('black', 'yellow'))

        # Als het niet de extensie .pcap heeft wordt er een melding teruggegeven
        else:
            Sg.Popup("Dit is geen Wireshark bestand.", button_color=('black', 'yellow'))

    def packet2array(self, filename):
        # hier wordt de functie aangeroepen uit de klasse met de constructor
        a = rdpcap(filename)
        x = ()
        for packet in a:
            y = (packet.summary().replace(';', '').replace('"', '').replace('/', '').replace('  ', ' '),)
            x = x + (y,)
        return x

# main uitvoeren
if __name__ == '__main__':
    Wireshark = Wireshark()
    print(Wireshark.packet2array("C:/Users/mzond/Desktop/DEV/TUF/example.pcap"))
