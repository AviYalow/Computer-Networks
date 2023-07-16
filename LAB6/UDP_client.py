import socket


my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.sendto('Omer'.encode(), ('127.0.0.1', 8821))
(data, remote_address) = my_socket.recvfrom(1024)
print('The server sent: ' + data.decode())
my_socket.close()

