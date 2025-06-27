import socket as Socket
import json
import uasyncio
import select

socket = None
current_temperature = 0.0


def init_listener(ip_addr, port):
    global socket
    address = (ip_addr, port)
    socket = Socket.socket()
    socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
    socket.bind(address)
    socket.listen()
    print(f"Socket bound and listening on {address[0]}:{address[1]} and listening")


def update_temperature(temp):
    global current_temperature
    current_temperature = temp


def handle_get_request(request):
    global current_temperature

    request = request.split('\r\n')

    if request:
        request_parts = request[0].split(' ')

        method = request_parts[0]
        path = request_parts[1]

        if method == "GET":
            if path == "/temp" or "/temperature":
                temp_data = {
                    "temperature": current_temperature,
                    "unit": "celsius"
                }

                response_body = json.dumps(temp_data)

                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "\r\n"
                    "{}"
                ).format(response_body)

                return response


async def check_listener_async():
    global socket
    while True:
        try:
            """
            select used to wait for blocking tasks, in this case i use it because
                of the blocking accept that would halt the program, waiting for someone to connect.
            Parameters: ([socket], [], [], 0)
                First list: sockets to check for incoming data
                Second list: sockets to check for outgoing data (empty cuz we dont care about outgoing data)
                Third list: sockets to check for errors (empty cuz i dont care about errors for now)
                0: timeout - return immediately, dont wait

            ready will contain [socket] if someone is trying to connect or [] if not
            """
            ready, _, _ = select.select([socket], [], [], 0)
            if ready:
                connection, return_address = socket.accept()
                connection.setblocking(False)  # sets the new connection to be not blocking

                ready_to_read, _, _ = select.select([connection], [], [], 0.5)
                if ready_to_read:
                    try: 
                        request = connection.recv(1024).decode()
                        print(f"Raw request:\n{request}")
                    except Exception as e:
                        print(f"recv failed: {e}")
                        connection.close()
                        return ("unknown", "none")
                else: 
                    print("No data ready")
                    connection.close()
                    return ("unknown", "none")

                if request.startswith("GET"):
                    response = handle_get_request(request)
                    connection.send(response.encode())
                    connection.close()
                    return ("get_request", "none")

                elif "\r\n\r\n" in request:
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

                connection.close()
                return ("unknown", "none")

            await uasyncio.sleep(0.01)

        except Exception as e:
            print(f"socket error: {e}")
            await uasyncio.sleep(0.1)


def check_listener():
    global socket
    connection, return_address = socket.accept()
    request = connection.recv(1024).decode()

    print(f"Raw request:\n {request}")

    if request.startswith("GET"):
        response = handle_get_request(request)
        connection.send(response.encode())
        connection.close()
        return ("get_request", "none")

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
