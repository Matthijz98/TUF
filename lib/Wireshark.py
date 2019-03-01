"""
Gemaakt door: Dylan Debipersad
Studentnummer: S1105887
"""

# Van de library scapy rdpcap en scapy_exception importeren
from scapy.all import rdpcap, Scapy_Exception
import os.path

# imports voor de GUI
import PySimpleGUI as Sg


# klasse Wrieshark aanmaken
class Wireshark:

    # functie aanmaken waarmee een packet wordt omgezet naar array om uit te kunnen lezen
    def packet_to_array(self, filename):
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
                Sg.Popup(f"Packets amount: {len(packets)}")

                # tuple aanmaken zodat die gevuld kan worden met packets
                packets_tuple = ()

                # voor elke packet moeten tekens (unicode) worden vervangen
                for packet in packets:
                    replace_unicode = (packet.summary().replace(';', '').replace('  ', ' '),)
                    # alles weer bij elkaar voegen
                    packets_tuple = packets_tuple + (replace_unicode,)
                # tuples returnen
                return packets_tuple

            # Dit vangt de error op om vervolgens een melding terug te geven
            except Scapy_Exception:
                # hier wordt er een foutmelding getoond
                Sg.Popup("This is not a valid Wireshark file.")

            # Als het bestand niet bestaat ook een foutmelding teruggeven
            except FileNotFoundError:
                # hier wordt er een foutmelding getoond
                Sg.Popup("This file doesn't exist.")

        # Als het niet de extensie .pcap heeft wordt er een melding teruggegeven
        else:
            Sg.Popup("This is not a valid Wireshark file.")


# main uitvoeren
if __name__ == '__main__':
    # klasse aanmaken van Wireshark
    Wireshark = Wireshark()

    # functie uitvoeren
    Wireshark.packet_to_array("testbestand")
