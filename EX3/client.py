import msvcrt
import select
import socket
import sys
from os import write

import protocol

def getInput(msg=""):
    """
    get input from the client.
    the function also handle with server responds
    :param msg: message to print -optional
    :return: the whole request from the client. in case he wants to exit return value is 'BYE'

    """
    if msg:
        print(msg)
    req=""
    while True:
        rlist, wlist, xlist = select.select([my_socket], [my_socket], [])
        for current_socket in rlist:
            valid_msg, rsp = protocol.get_msg(my_socket)
            if valid_msg:
                print("Server sent: " + rsp)
                if rsp == "BYE":
                    return "BYE"
            else:
                print("invalid message")
        if msvcrt.kbhit():
                ch = msvcrt.getch().decode("utf-8")
                if ch == '\r':
                    print()
                    break
                if ch == '\b':
                    req =req[:-1]
                    sys.stdout.write("\b")
                else:
                    req += ch
                    print(ch, flush=True,end="")
    return req

my_socket = socket.socket()

my_socket.connect(("127.0.0.1", protocol.PORT))

req = getInput("Pls enter commands\n")

while True:
    if req == "BYE":
        break
    req = protocol.create_msg(req)
    my_socket.send(req.encode())
    req = getInput()



print("Closing\n")
my_socket.close()