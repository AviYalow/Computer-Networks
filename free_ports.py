from scapy.all import *

SYN = 0x02
ACK = 0x10

syn_segment = TCP(dport=443, seq=123 , flags='S')
syn_packet = IP(dst='8.8.8.8')/syn_segment


for port in range(80,90):
     print(f'loop number: {port}')
     syn_packet[TCP].dport=port
     try:
        syn_ack_packet = sr1(syn_packet,verbose=0,timeout=0.5)
        F = syn_ack_packet['TCP'].flags
        if F&SYN and F&ACK:
             print(f'listing on port {port}')
     except:
         continue

import socket

target = "127.0.0.1"  # Replace with the IP address or hostname of the target machine
port_range = range(1, 65536)  # Scan all ports from 1 to 1024

for port in port_range:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)  # Set a timeout of 100 milliseconds
    try:
        s.connect((target, port))
    except Exception as e:
        print(f"Port {port} is closed")
    else:
        print(f"Port {port} is open")
        s.close()