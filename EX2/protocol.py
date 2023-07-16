"""EX 2.6 protocol implementation
   Author: Avi Yalow
   Date: 7.11.2022
   Possible client commands:
   NUMBER - server should reply with a random number, 0-99
   HELLO - server should reply with the server's name, anything you want
   TIME - server should reply with time and date
   EXIT - server should send acknowledge and quit
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820
VALID_COMMANDS = ["NUMBER", "HELLO", "TIME", "EXIT"]

"""
Create a valid protocol message, with length field
e.g. "05HELLO"
"""


def create_msg(data):
    prefix = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return prefix + data


"""Extract message from protocol, without the length field
 If length field does not include a number, returns False, "Error" """


def get_msg(client_socket):
    data_len = client_socket.recv(LENGTH_FIELD_SIZE).decode()
    if data_len.isdigit():
        data = client_socket.recv(int(data_len)).decode()
        return True, data
    else:
        return False, "Error"
