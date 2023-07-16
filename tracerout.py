from scapy.all import *
import sys

"""
tracerout
"""
destination = "8.8.8.8" #sys.argv[1]
i=1
while True:
    packet = IP(ttl=i, dst=destination) / ICMP()
    try:
        res = sr1(packet,verbose=0,timeout=2)
        print(res[IP].src)
        if res[ICMP].type == 0: # ECHO REPLY /8 = REQUEST
            break
    except:
       print("no response")
    i += 1