LENGTH_FIELD_SIZE = 2
PORT = 5555
VALID_COMMANDS = ["NAME", "GET_NAMES", "MSG", "EXIT"]


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    prefix = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return prefix + data


def get_msg(client_socket):
    """Extract message from protocol, without the length field
     If length field does not include a number, returns False, "Error" """

    data_len = client_socket.recv(LENGTH_FIELD_SIZE).decode()
    if data_len.isdigit():
        data = client_socket.recv(int(data_len)).decode()
        return True, data
    else:
        return False, "Error"
