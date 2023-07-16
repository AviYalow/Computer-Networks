"""EX 2.6 server implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""

import socket
import protocol


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    return "Server response"


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g NUMBER, HELLO, TIME, EXIT)"""
    return True


def main():
    # Create TCP/IP socket object

    # Bind server socket to IP and Port

    # Listen to incoming connections

    print("Server is up and running")
    # Create client socket for incoming connection

    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            # 2. Check if the command is valid, use "check_cmd" function
            # 3. If valid command - create response

        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage


        # Send response to the client


        # If EXIT command, break from loop

    print("Closing\n")
    # Close sockets


if __name__ == "__main__":
    main()
