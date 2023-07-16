"""EX 2.6 server implementation
   Author: Avi Yalow
   Date: 7.11.2022
   Possible client commands defined in protocol.py
"""
import datetime
import socket
import random

import protocol

"""Based on the command, create a proper response"""


def create_server_rsp(cmd):
    if cmd == "NUMBER":
        rsp = str(random.randint(0, 99))
    if cmd == "HELLO":
        rsp = "Hello I'm SuperServer"
    if cmd == "TIME":
        rsp = datetime.datetime.now()
        rsp = rsp.strftime("%d-%m-%Y %H:%M:%S")
    if cmd == "EXIT":
        rsp = "BYE"
    return rsp


"""Check if the command is defined in the protocol
 (e.g. NUMBER, HELLO, TIME, EXIT)"""


def check_cmd(data):
    if data in protocol.VALID_COMMANDS:
        return True
    else:
        return False


def main():
    # Create TCP/IP socket object
    server_socket = socket.socket()

    # Bind server socket to IP and Port
    server_socket.bind(('0.0.0.0', protocol.PORT))

    # Listen to incoming connections
    server_socket.listen()
    print("Server is up and running")

    # Create client socket for incoming connection
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:

        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:

            # 1. Print received message
            print(cmd)

            # 2. Check if the command is valid, use "check_cmd" function
            # 3. If valid command - create response
            if check_cmd(cmd):
                response = create_server_rsp(cmd)
            else:
                response = "invalid command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        rsp = protocol.create_msg(response)
        client_socket.send(rsp.encode())

        # If EXIT command, break from loop
        if cmd == "EXIT":
            break

    print("Closing\n")

    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
