# python c:\networks\work\networksbook\multiclient\chat_client.py
import socket
import select
import msvcrt
# NAME <name> will set name. Server will reply error if duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
print("Pls enter commands\n")
msg = ""
while msg != "EXIT":
    rlist, wlist, xlist = select.select([my_socket], [], [], 0.1)
    if rlist:
        data = my_socket.recv(1024).decode()
        print("Server sent: ", data)
    if msvcrt.kbhit():
        char = msvcrt.getch().decode()
        print(char, end="", flush=True)
        msg += char
        if char == "\r":
            print()
            my_socket.send(msg.encode())
            msg = ""

my_socket.close()

