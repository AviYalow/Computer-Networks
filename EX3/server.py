import socket
import select
import protocol

SERVER_IP = '0.0.0.0'


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
server_socket.bind((SERVER_IP, protocol.PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
client_names_by_socket = {}
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [server_socket] + client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            valid_msg, cmd = protocol.get_msg(current_socket)
            if valid_msg:
                if cmd == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    client_names_by_socket.pop(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    messages_to_send.append((current_socket, cmd))
            else:
                response = "Wrong protocol"
                current_socket.recv(1024)


    for message in messages_to_send:
        """
        function to handle with the message from the clients
        the server will create response and send it to the 
        correct client
        """
        current_socket, cmd = message
        if current_socket in wlist:
            print(cmd)
            cmd = cmd.split(" ")
            """
            cmd is the client command. we separate the command and extract it to list
             in order to control the command.
             for example: index 0- type of the command
            """
            cmd_type = cmd[0]

            if cmd_type == "NAME" and len(cmd) == 2:
                client_name = cmd[1]
                if client_name not in client_names_by_socket.values():
                    client_names_by_socket[current_socket] = client_name
                    res = "Hello " + client_name
                else:
                    res = "This name is already exist"
                res = protocol.create_msg(res)
                current_socket.send(res.encode())

            elif cmd_type == "GET_NAMES" and len(cmd) == 1:
                res = " ".join([name for name in client_names_by_socket.values()])
                res = protocol.create_msg(res)
                current_socket.send(res.encode())

            elif cmd_type == "MSG" and len(cmd) >= 3:
                src_name = client_names_by_socket[current_socket]
                dst_name = cmd[1]
                if dst_name in client_names_by_socket.values():
                    dst_socket = find_socket_by_name(dst_name)
                    res = client_names_by_socket[current_socket] + " sent " + " ".join(cmd[2:])
                    res = protocol.create_msg(res)
                    dst_socket.send(res.encode())
                else:
                    res = "This name doesn't exist"
                    res = protocol.create_msg(res)
                    current_socket.send(res.encode())

            elif cmd_type == "EXIT":
                res = "BYE"
                client_sockets.remove(current_socket)
                del client_names_by_socket[current_socket]
                res = protocol.create_msg(res)
                current_socket.send(res.encode())
            else:
                res = "command is not supported"
                res = protocol.create_msg(res)
                current_socket.send(res.encode())
            if message:
                messages_to_send.remove(message)
