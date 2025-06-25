import socket as Socket


address = ('0.0.0.0', 80)
socket = Socket.socket()
socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
socket.bind(address)
socket.listen()
print(f"socket bound to {address[0]}:{address[1]} and listening")


while True:
    connection, return_address = socket.accept()
    request = connection.recv(1024).decode()
    request_data = request.split('\r\n')[-1]
    print(request_data)
