from server import Server

if __name__ == "__main__":
    host = '192.168.0.193'
    port = 8082
    server = Server(port, host)

import socket
print (socket.gethostname())

print (socket.gethostbyname(socket.gethostname()))