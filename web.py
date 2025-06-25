import socket as Socket
import json
socket = None


def init_listener(ip_addr, port):
    global socket
    address = (ip_addr, port)
    socket = Socket.socket()
    socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
    socket.bind(address)
    socket.listen()
    print(f"Socket bound and listening on {address[0]}:{address[1]} and listening")


def check_listener():
    global socket
    connection, return_address = socket.accept()
    request = connection.recv(1024).decode()

    print(f"Raw request:\n {request}")

    if "\r\n\r\n" in request:
        request_data = request.split('\r\n\r\n')[1]
        print(f"Extracted data:\n{request_data}")

        json_data = json.loads(request_data)

        device = json_data.get("device")
        notify_level = json_data.get("notify")

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Connection: close\r\n"
            "\r\n"
            "POST received and parsed successfully"
        )

        connection.send(response.encode())
        connection.close()

        return (device, notify_level)

    response = (
        "HTTP/1.1 400 Bad Request\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n"
        "\r\n"
        "POST received but failed to parse"
    )

    connection.send(response.encode())
    connection.close()
    return ("unknown", "none")
