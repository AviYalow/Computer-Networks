from scapy.all import *


request_packet = IP(dst="8.8.8.8", ttl=0)/ICMP()/"hello"
hop=1

while(request_packet[IP].src!="8.8.8.8"):
    print(f'hop number: {hop}')
    try:
        response_packet = sr1(request_packet,verbose=0, timeout=2)
        print(response_packet[IP].src)
    except:
        print("no response")
    hop+=1
    request_packet[IP].ttl=hop

print(f'number of hops to google {hop}')