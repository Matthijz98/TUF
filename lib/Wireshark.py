"""
Gemaakt door:
Studentnummer:
"""
# Van de library scapy alles importeren
from scapy.all import *

# rdpcap importeren van scapy. Dit laadt de file in.
# voer hier het pad naar de file in
packets = rdpcap('')

# Hier worden het aantal packets getoond
print("Aantal packets:", len(packets))

# Hier wordt elke packet getoond
for packet in packets:
    packets.show()
    break
