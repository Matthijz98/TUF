from scapy.all import *

# rdpcap importeren van scapy. Dit laadt de file in.
# voer hier het pad naar de file in
packets = rdpcap('')

print(len(packets))

# elke packet wordt getoond
for packet in packets:
    packets.show()
    break
    #print(packets)
