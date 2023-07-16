import random
import socket

MAX_MSG_LENGTH = 1024
PORT = 5555


while True:
    my_socket = socket.socket()

    my_socket.connect(("127.0.0.1", PORT))
    request = str(random.randint(0, 99))
    my_socket.send(request.encode())
    respond = my_socket.recv(MAX_MSG_LENGTH).decode()
    print("The server sent " + respond)



my_socket.close()