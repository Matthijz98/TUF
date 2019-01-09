from scapy.all import *

# rdpcap importeren van scapy. Dit laadt de file in.
# voer hier het pad naar de file in
packets = rdpcap("")

# elke packet wordt getoond
for packet in packets:
    print(packets)
