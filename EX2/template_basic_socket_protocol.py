"""EX 2.6 protocol implementation
   Author:
   Date:
   Possible client commands:
   NUMBER - server should reply with a random number, 0-99
   HELLO - server should reply with the server's name, anything you want
   TIME - server should reply with time and date
   EXIT - server should send acknowledge and quit
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820


def create_msg(data):
    """Create a valid protocol message, with length field"""
    return "05HELLO"


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    return True, "HELLO"
