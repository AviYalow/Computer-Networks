from collections import Counter
from scapy.all import *

SYN = 0x02
ACK = 0x10
syn_count = Counter()
ack_count = Counter()


pcapFile = rdpcap("SYNflood.pcapng")
output_file = open("suspect_ips.txt",'w')


# count all the SYN packets that destined to our organization
for pkt in pcapFile:
    if TCP in pkt:
        F = pkt['TCP'].flags
        if F & SYN and not F & ACK and "100.64" in pkt[IP].dst:
            syn_count[pkt[IP].src] += 1

# count all the ACK packets that destined to our organization
for pkt in pcapFile:
    if TCP in pkt:
        F = pkt['TCP'].flags
        if not F & SYN and F & ACK and "100.64" in pkt[IP].dst:
            ack_count[pkt[IP].src] += 1


# for each ip address that sent a syn,if it sent syn more than 9 times, and
# it didn't send an ack, it suspects as an attack ip address
for suspect_ip in syn_count:
    if syn_count[suspect_ip] > 9 and suspect_ip not in ack_count.keys():
        output_file.write(suspect_ip+"\n")


output_file.close()