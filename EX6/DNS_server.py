import socket
from scapy.all import *
import re

DEFAULT_RESPOND = "About DNS Lookup\n" \
                  "DNS Lookup is a browser based network tool that displays DNS records showing publicly for the domain name being queried." \
                  "\nDNS Lookup allows you to use public DNS server (Google, Cloudflare, Quad9, OpenDNS, Level3, Verisign, Comodo, Norton, Yandex, NTT, SDNS, CFIEC, Alidns, 114DNS, Hinet, etc.), " \
                  "Specify name server, Authoritative name server, Top-level domain name server, Root name server and other DNS servers for query. These DNS server IP addresses support IPv4 and IPv6." \
                  "\nEnable Advanced Mode displays the authority, additional, DNS message header, and DNS server response information for the DNS query. " \
                  "This can help to understand more comprehensive DNS Lookup information." \
                  "\nEnable DNSSEC (Domain Name System Security Extensions), DNSSEC creates a secure domain name system by adding cryptographic signatures to existing DNS records." \
                  " By checking its associated signature, you can verify that a requested DNS record comes from its authoritative name server and wasn’t altered en-route, opposed to a fake record" \
                  " injected in a man-in-the-middle attack."

LISTENING_IP = '0.0.0.0'
PORT = 8153
PROTOCOL_VERSION = "HTTP/1.1"
SOCKET_TIMEOUT = 0.1
STATUS_CODE_OK = " 200 OK"
IP_ADDRESS_PATTERN = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
ERROR_TYPE_A = "DNS request failed: The domain name referenced in the query does not exist."
ERROR_TYPE_PTR = "DNS request failed: The ip referenced in the query does not exist."


def nslookup_type_A(url):
    """
       handle with a type A nslppkup query
       :param url: domain name query
       :return: ip address
       """
    answer = sr1(IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=url)), verbose=False)
    response = ""
    print(answer[DNS].summary())
    if answer[DNS].qd.qtype == 1:
        for x in range(answer[DNS].ancount):
            if re.match(IP_ADDRESS_PATTERN, str(answer[DNS].an[x].rdata)) is None:
                continue
            response += answer[DNS].an[x].rdata + "\n"
    if response == "":
        response = ERROR_TYPE_A
    return response


def nslookup_type_PTR(ip):
    """
    handle with a type PTR nslppkup query
    :param ip: ip query
    :return: domain name
    """
    answer = sr1(IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qtype="PTR", qname=ip + ".in-addr.arpa")),
                 verbose=False)
    response = ""
    print(answer[DNS].summary())
    print(answer[DNS].qd.qtype)
    if answer[DNS].qd.qtype == 12:
        for x in range(answer[DNS].ancount):
            dn = answer[DNS].an[x].rdata.decode()
            index = dn.find(".")
            dn = dn[index + 1:]
            response += dn + "\n"
    if response == "":
        response = ERROR_TYPE_PTR
    return response


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""

    # building the response header. the template: http version, status code ,optional filed, data.
    http_header = PROTOCOL_VERSION + STATUS_CODE_OK + "\r\n"

    try:
        if resource == '':
            data = DEFAULT_RESPOND
        elif "reverse" in resource:
            resource = resource[len("reverse") + 1:]
            data = nslookup_type_PTR(resource)
        else:
            data = nslookup_type_A(resource)
    except Exception as e:
        data = "Error: {}".format(e)

    content_len = "Content-Length: " + str(len(data)) + "\r\n"

    http_response = (http_header + content_len + "\r\n" + data).encode()

    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # Extracting the first line of the request and separating it

    method, url, version = request.split("\r\n")[0].split()
    if method == "GET" and version == PROTOCOL_VERSION:
        return True, url[1:]
    else:
        return False, url[1:]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP,
     calls function to handle the requests """
    print('Client connected')
    while True:
        try:
            client_request = client_socket.recv(1024).decode()
        except socket.error as socEr:
            print("ERROR: {}".format(socEr))
            continue
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTENING_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))
    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
