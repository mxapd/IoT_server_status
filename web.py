import socket as Socket
import json
import uasyncio
import select

socket = None


def init_listener(ip_addr, port):
    global socket
    address = (ip_addr, port)
    socket = Socket.socket()
    socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
    socket.bind(address)
    socket.listen()
    socket.setblocking(False)
    print(f"Socket bound and listening on {address[0]}:{address[1]} and listening")


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
                connection.setblocking(False) # sets the new connection to be not blocking

                # Wait for data to be available on the connection
                request_data = b""
                max_attempts = 100  # Prevent infinite loop
                attempts = 0
                
                while attempts < max_attempts:
                    try:
                        conn_ready, _, _ = select.select([connection], [], [], 0)
                        if conn_ready:
                            chunk = connection.recv(1024)
                            if chunk:
                                request_data += chunk
                                # Check if we have a complete HTTP request
                                if b'\r\n\r\n' in request_data:
                                    break
                            else:
                                # Connection closed by client
                                break
                        else:
                            # No data available yet, yield control
                            await uasyncio.sleep(0.01)
                            attempts += 1
                    except OSError as e:
                        if e.args[0] == 11:  # EAGAIN - no data available
                            await uasyncio.sleep(0.01)
                            attempts += 1
                            continue
                        else:
                            raise

                if request_data:
                    request = request_data.decode('utf-8', errors='ignore')
                    print(f"Raw request:\n {request}")

                    if "\r\n\r\n" in request:
                        body_data = request.split('\r\n\r\n')[1]
                        print(f"Extracted data:\n{body_data}")

                        try:
                            json_data = json.loads(body_data)
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
                        
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e}")
                            response = (
                                "HTTP/1.1 400 Bad Request\r\n"
                                "Content-Type: text/plain\r\n"
                                "Connection: close\r\n"
                                "\r\n"
                                "Invalid JSON data"
                            )
                            connection.send(response.encode())
                            connection.close()
                            return ("unknown", "none")

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
