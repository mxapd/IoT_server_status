![image](https://github.com/user-attachments/assets/70bd95cb-3584-42bf-8620-0944b9b9b5b0)# Network Device Status and Notification Device 

**Author:** Max Porseryd (mp224hv)  
**Course:** 1DT305 - Introduction to Applied Internet of Things  
**Date:** 30 June 2025

**Estimated Time**: 2h

## Project Overview

I built a network monitoring system using a Raspberry Pi Pico W that watches my home network devices and shows their status with colored LEDs. It keeps an eye on my server, PC, and specific services on the server like Jellyfin, then lights up green when everything's working or red when something's down. 

It hosts an HTTP API, so other systems can send it notifications to trigger different LED patterns. Useful for seeing at a glance if my home lab is having issues without having to check a bunch of different dashboards or log into anything, its just right there on my wall. Currently i have four levels of notifications, none (led of), info (on), warning (slowly blinking) and critical (triple blink every couple of seconds). 

Another feature is a temperature sensor on the pico that reads the room temperature which is retrievable from the HTTP API, this is a bit of a tack on because of the course requirements but it will come in handy as i dont have another temperature sensor anywhere in my appartment. 

## Objective

### Why This Project?

Honestly, I got tired of my server randomly going down and not knowing about it until I tried to use something. I wanted something simple that would just tell me "hey, your stuff is broken" without having to open up some webpage or other monitoring tool, just a quick glance at my wall or whereever i put this and know if i need to log into a device to fix or look at something.

### Purpose and Benefits

The main goals were:
- Quick visual feedback - I can just glance at the LEDs and know if something's wrong
- Catch problems early - Better to know about issues before they affect what I'm doing
- Monitor specific services - Not just "is the server on" but "is Jellyfin actually running"
- Accept external notifications - Other scripts can tell it to flash lights for warnings so i can know if my server is overheating or something else. 
- Learn - Good excuse to learn how to work with microcontrollers and other IoT concepts.

### Expected Insights

The system provides insights into:
- How my networked devices are doing, if they are up and if they have any important notifications/events. 
- Current temperature of my apartment

## Material

### Components Used

| Component | Purpose | Specifications | Source | 
|-----------|---------|----------------|---------|
| Raspberry Pi Pico W | Main microcontroller | ARM Cortex-M0+, 264KB RAM, WiFi | Electrokit |
| LEDs (Red/Green/Yellow) | Status indicators | 3mm, 20mA, 2.0-2.2V forward voltage | Electrokit |
| Resistors | Current limiting | 1000Ω | Electrokit |
| Breadboard | Wiring Platform | 840 connection points | Electrokit |
| Jumper wires | Connections | Male-to-male, various colors | Electrokit |
| USB Cable | Programming/Power | Micro-USB to USB-A | Electrokit |
| MCP9700 TO-92 Temperature Sensor | Read the temprerature | 2.3-5.5VDC | Electrokit |

**Total Cost: 349kr** (for the start kit bundle) + shipping 

### Component Details

**Raspberry Pi Pico W:** The heart of the system, chosen for its built-in WiFi capability, sufficient GPIO pins for multiple LEDs, and native MicroPython support. 

**LEDs:** Standard 3mm LEDs provide clear visual indication. Colors chosen follow common conventions:
- Red: Device/service down or error state
- Green: Device/service operational
- Yellow: Warning/notification state

**Resistors:** 1000Ω resistors limit current to safe levels for LEDs, ensuring longevity and preventing damage.

**Temperature Sensor**: Reads the ambient temperature.

## Computer Setup

### Development Environment

My development environment is centered around **Neovim**. I use it as my main editor alongside a Python LSP for code intelligence.

When working with MicroPython, I don’t use any special plugins just a standard Python LSP. To interface with the Raspberry Pi Pico, I use **mpremote**, a terminal tool that makes it easy to upload files and access the Pico REPL.

For managing project-specific dependencies like mpremote or python3, I use nix-shell. Each project includes a shell.nix file that declares the necessary packages. When I run nix-shell, the required tools are installed in a temporary isolated environment. This ensures that all dependencies are tied directly to the project, making it easy to get started, just enter the development shell and everything is ready to go.

If you're curious, you can explore my full setup here: https://github.com/mxapd/nix.

### Installation Steps

#### IDE and development environment
Installing and configuring neovim is not something i want to go into here since it goes outside the scope for this report. All my configuration files can be found in my nix repo above. 

To install python and mpremote i use a nix-shell as mentioned, to follow along with that method all you need to do is copy that file, put it in your project directory and run `$ nix-shell`. 

(OBS requires you to be on nixos or have the nix package manager, if you dont want to do that just install in some other way) 

While in the development shell python and mpremote are availible to use. 

#### Setting up Pico for MicroPython

Next is setting up and preparing the pico for programming with micropython.  

1. Download the firmware from https://micropython.org/download/RPI_PICO_W/
2. Plug in your microUSB cable into the pico and then hold BOOTSEL while plugging it in to a computer.
3. Copy the .uf2 file into the mass storage device that appears. The pico will now install the firmware and automaticly reset, after which it is ready for use.

Now to upload code all we need to do is use mpremote, the exact command to copy files is:
``
$ sudo mpremote connect auto fs cp <filename> : # copy files to pico
``
``
$ sudo mpremote connect auto repl # connect to the repl to run commands
``

## Putting Everything Together

### Circuit Design

The circuit follows a simple design connecting multiple LEDs to GPIO pins through current-limiting resistors.

```
Pico W GPIO Layout:
├── Pin 3 (GND)     → Common ground for all LEDs and sensors
├── Pin 4 (GP2)     → 1000Ω → Red LED     (Server status)
├── Pin 5 (GP3)     → 1000Ω → Green LED   (Server status)  
├── Pin 6 (GP4)     → 1000Ω → Yellow LED  (Server notifications)
├── Pin 9 (GP6)     → 1000Ω → Red LED     (PC status)
├── Pin 10 (GP7)    → 1000Ω → Green LED   (PC status)
├── Pin 11 (GP8)    → 1000Ω → Yellow LED  (PC notifications)
├── Pin 14 (GP10)   → 1000Ω → Green LED   (Jellyfin service)
├── Pin 15 (GP11)   → 1000Ω → Red LED     (Jellyfin service)
├── Pin 19 (GP14)   → 1000Ω → Green LED   (Web service)
├── Pin 20 (GP15)   → 1000Ω → Red LED     (Web service)
├── Pin 31 (ADC0)   → Temp Sensor (middle leg of sensor flat facing)
└── Pin 36 (3V3OUT) → Temp Sensor (left leg of sensor flat facing)
```
![image](https://github.com/user-attachments/assets/8775fe92-ab12-4e21-891a-960a49d7be74)


### Electrical Calculations

Equation for the temperature sensor: 
- Voltage = (ADC reading * 3.3) / 65535
- Temperature = (Voltage - 0.5) * 100

## Platform Choice

### How I Set Things Up

For this project, i chose not to use a third-party or cloud-based platform. Instead, i developed a fully self-hosted and self-made solution running entirely on the Raspberry Pi Pico W. This decision was driven by my interest in building systems from the ground up and avoiding reliance on external services or subscriptions.

By keeping everything local and self-contained, i ensure full ownership of the system, greater privacy, and no ongoing costs.

Key advantages of this approach:
- All the monitoring logic runs on the Pico W
- LEDs respond immediately 
- Works even if internet goes down
- No monthly fees or cloud dependencies
- Simple HTTP API for recieving notifications
- Could hook into other monitoring tools if I wanted
- Easy to write scripts that send alerts

Currently, this setup handles my small home network just fine. If I wanted to scale it up, I believe my self-made system could still work, but I would need to:
- Improve error handling
- Harden the code against edge cases and bugs
- Possibly explore external options for reliability or convenience

Since everything depends on my own code and design, the system’s ability to scale is entirely up to me and the effort I put into maintaining and extending it.

## The Code

The whole thing runs using Python's `uasyncio` library, which lets me do multiple things at once without getting complicated (which makes it so i can controll LEDs, listen for connections, handle requests, and monitor devices all without blocking the program which makes it appear as everything happening at the same time).

### Network Setup
```python
def connect_wifi(ssid, key):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, key)

    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)

    if wlan.status() != 3:
        print('Failed to establish a network connection')
        return 1
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return network_info```

This establishes WiFi connection with a 10-second timeout mechanism. Returns network configuration on success or an error code on failure.

### Host monitoring

def check_host(host, port=22, timeout=1):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except Exception as e:
        return False
```

This is a network connectivity checker that attempts to establish a TCP connection to verify if a host/service is reachable. It's used to monitor multiple services (SSH, HTTP, Jellyfin) on different ports. 

### Temperature Sensor Calculation

```python
def read_temp():
    tempsens = ADC(Pin(26))
    reading = tempsens.read_u16()
    voltage = reading * 3.3 / 65535  # convert to voltage (0-3.3V)
    temp_c = (voltage - 0.5) * 100  # convert voltage to temperature in °C
    return temp_c

```

This function reads from the temperature sensor, converts the 16-bit ADC reading to voltage, then applies a temperature conversion formula which was found in the sensors documentation.

### Asynchronous Web Server

```python
async def check_listener_async():
    global socket
    while True:
        try:
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
                
                # then processess the get/post request ... 
```

This is one of the more complicated functions since it uses uses `select()` to implement non-blocking socket operations on a typically blocking operation, allowing the microcontroller to handle web requests without halting the monitoring loop. 

### Priority based notification system

```python
NOTIFICATION_PRIORITIES = {"none": 0, "info": 1, "warning": 2, "critical": 3}

async def handle_notification(device_name, notify_level):
    current_priority = device_priority_levels.get(device_name, 0)
    new_priority = NOTIFICATION_PRIORITIES.get(notify_level, 0)
    
    if notify_level == "none" or new_priority > current_priority:
        # cancel existing notification task
        if device_name in notification_tasks:
            notification_tasks[device_name].cancel()
        
        # set new notification pattern
        if notify_level == "warning":
            task = uasyncio.create_task(blink_led(yellow_pin, 1.0, 1.0))
        elif notify_level == "critical":
            task = uasyncio.create_task(critical_blink(yellow_pin))
```

This implements a priority system where higher-priority notifications override lower ones. Uses asyncio tasks for different LED patterns (on, slow blink, triple blink).


### Core Libraries

- machine: hardware controls like for sending voltage across pins and reading adc
- network: wifi connectivity
- socket: tcp connection testing for checking hosts and hosting a simple web server
- uasyncio: asynchronous programming capabilities
- select: non blocking socket operations
- json: api data parsing

## Connectivity

### Transmitting Data

The system primarily performs outbound monitoring rather than transmitting sensor data to external servers. However, it does expose temperature data via HTTP API:

```python
def handle_get_request(request):
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
```
### Recieving data (notifications)

The device receives notifications via HTTP POST requests and expects following format:
```python
{
    "device": "server",
    "notify": "warning"
}
```
### Wireless protocol: WiFi

I chose to use WiFi since i wanted this to be a monitor for my home network and using WiFi to establish a direct link to my network made alot of sense.

Implementation:

```python
def connect_wifi(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, key)
```
### Transport Protocol: HTTP/TCP

Monitoring hosts:
```python
def check_host(host, port=22, timeout=1):
    sock = socket.socket()  # TCP socket
    sock.settimeout(timeout)
    sock.connect((host, port))  # Direct TCP connection test
```

API Server:

```python
init_listener(ip_addr, 80) # http server on port 80, handles both get (temperature) and post (notifications) requests

def init_listener(ip_addr, port):
    global socket
    address = (ip_addr, port)
    socket = Socket.socket()
    socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
    socket.bind(address)
    socket.listen()
    print(f"Socket bound and listening on {address[0]}:{address[1]}")
```

## Presenting the data

### The LED Dashboard

The main interface is just the LEDs themselves. I can glance over and immediately see what's going on:

**LED Patterns:**
- **Solid Green:** Everything's working fine
- **Solid Red:** Something's broken or unreachable
- **Solid Yellow:** General info notification
- **Slow blinking Yellow:** Warning level
- **Fast triple-blink Yellow:** Critical alert

### Data Storage (Or Lack Thereof)

Right now I'm not saving any historical data - it's purely a real-time status display. All the debugging info goes to the serial console while I'm developing, but that's about it. Altough i will probably add a simple logging system to save debugging info to a database or a logfile. 

### Future Ideas

If I wanted to get fancier, I could easily add:
- **Local database** to track uptime statistics and historical temperature readings
- **Web interface** showing current status and graphs
- **Integration with home automation** to do things like restart services when they fail

But honestly, just having the LEDs has been surprisingly useful. Sometimes simple is better.

## Final Results

![device_monitor_device](https://github.com/mxapd/IoT_server_status/blob/main/images/IMG_20250708_141524572.jpg)

---

**Code Repository:** https://github.com/mxapd/IoT_server_status  
