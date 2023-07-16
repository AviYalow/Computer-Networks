import socket

MAX_MSG_LENGTH = 1024
PORT = 5555

my_socket = socket.socket()

my_socket.connect(("127.0.0.1", PORT))

request = input("Please enter your name:")
while True:
    if request == "":
        break

    my_socket.send(request.encode())
    respond = my_socket.recv(MAX_MSG_LENGTH).decode()
    print("The server sent " + respond)

    request = input("Please enter your name:")

my_socket.close()
