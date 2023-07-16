import socket
import select
from scapy.all import *
import re

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555
IP_ADDRESS_PATTERN = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
ERROR_TYPE_A = "DNS request failed: The domain name or the client name referenced in the query does not exist."


def remove_socket(curr_socket):
    print("Connection closed")
    client_sockets.remove(curr_socket)
    del client_names_by_socket[curr_socket]
    curr_socket.close()
    print_client_sockets(client_sockets)


def nslookup_type_A(url):
    """
       handle with a type A nslookup query
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
            response += ("\n" + answer[DNS].an[x].rdata)
    if response == "":
        response = ERROR_TYPE_A
    return response


def find_socket_by_name(name):
    """
    find a specific client socket by his name
    :param name: name of the client
    :return: client socket
    """
    return [sct for sct in client_names_by_socket if client_names_by_socket[sct] == name][0]


def print_client_sockets(client_sockets):
    """
    print the available client
    :param client_sockets: list of sockets
    """
    for c in client_sockets:
        print("\t", c.getpeername())


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
client_names_by_socket = {}
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [server_socket] + client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:  # if server_socket redy to read its mean that there is a new client
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)

        else:  # handle with clients requests
            try:
                data = current_socket.recv(1024).decode()
                if data == "":
                    remove_socket(current_socket)
                else:
                    print(f'received data: {data}')  # log print for debug
                    if data and data[-1] == "\r":
                        data = data[:-1]

                    messages_to_send.append((current_socket, data))
            except:
                remove_socket(current_socket)

    for message in messages_to_send:
        """
        handling clients messages.
        the server will create response and send it to the 
        correct client
        """
        current_socket, cmd = message
        if current_socket in wlist:
            print(cmd)
            """
            cmd is the client command. we separate the command and extract it to list
             in order to control and validate the command.
             for example: index 0 is the type of the command
            """
            cmd = cmd.split(" ")
            cmd_type = cmd[0]

            if cmd_type == "NAME" and len(cmd) == 2:
                client_name = cmd[1]

                if client_name not in client_names_by_socket.values():
                    client_names_by_socket[current_socket] = client_name
                    res = "Hello " + client_name
                else:
                    res = "This name is already exist"

                current_socket.send(res.encode())

            elif cmd_type == "GET_NAMES" and len(cmd) == 1:
                res = " ".join([name for name in client_names_by_socket.values()])
                current_socket.send(res.encode())

            elif cmd_type == "MSG" and len(cmd) >= 3:
                src_name = client_names_by_socket[current_socket]
                dst_name = cmd[1]
                if dst_name in client_names_by_socket.values():
                    dst_socket = find_socket_by_name(dst_name)
                    res = client_names_by_socket[current_socket] + " sent " + " ".join(cmd[2:])
                    dst_socket.send(res.encode())
                else:
                    res = "This name doesn't exist"
                    current_socket.send(res.encode())

            elif cmd_type == "EXIT":
                # client wants to close connection
                print("Connection closed")
                current_socket.close()
                client_sockets.remove(current_socket)
                del client_names_by_socket[current_socket]
                print_client_sockets(client_sockets)

            elif cmd_type == "NSLOOKUP" and len(cmd) == 2:
                target = cmd[1]
                if target in client_names_by_socket.values():
                    target_socket = find_socket_by_name(target)
                    res = target_socket.getpeername()[0]
                    current_socket.send(res.encode())
                else:
                    res = nslookup_type_A(target)
                    current_socket.send(res.encode())

            else:
                res = "command is not supported"
                current_socket.send(res.encode())
            if message:
                messages_to_send.remove(message)
