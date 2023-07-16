from scapy.all import *

#if we sending with ethernet manual
#srp1
#sendp(my_layer2_packet)

my_layer2_packet = ARP(pdst="192.168.43.1")# req
my_layer2_packet.show()

ans= sr1(my_layer2_packet)

ans.show()

print(ans[ARP].op)