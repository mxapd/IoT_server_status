from machine import Pin
import time
from secrets import WIFI_SSID, WIFI_PASSWORD
from lib import connect_wifi, check_host, read_temp

UPDATE_INTERVAL = 30

devices = {
    "server": {
        "red": Pin(2, Pin.OUT),
        "green": Pin(3, Pin.OUT),
        "yellow": Pin(4, Pin.OUT),
        "ip": "192.168.1.251",
        "ports": [80, 22, 443, 8096],
    },
    "server_jellyfin": {
        "red": Pin(11, Pin.OUT),
        "green": Pin(10, Pin.OUT),
        "ip": "192.168.1.251",
        "ports": [8096],
    },
    "server_web": {
        "red": Pin(15, Pin.OUT),
        "green": Pin(14, Pin.OUT),
        "ip": "192.168.1.251",
        "ports": [80],
    },
    "pc": {
        "red": Pin(6, Pin.OUT),
        "green": Pin(7, Pin.OUT),
        "yellow": Pin(8, Pin.OUT),
        "ip": "192.168.1.208",
        "ports": [22],
    }
}


for device in devices.values():
    for color in ["red", "green", "yellow"]:
        if color in device:
            device[color].value(0)

if connect_wifi(WIFI_SSID, WIFI_PASSWORD) == 0:
    for _ in range(3):
        devices["server"]["green"].value(1)
        time.sleep(0.5)
        devices["server"]["green"].value(0)
        time.sleep(0.5)
else:
    for _ in range(3):
        devices["server"]["red"].value(1)
        time.sleep(0.5)
        devices["server"]["red"].value(0)
        time.sleep(0.5)
    raise RuntimeError("Failed to establish network connection")

while True:
    temperature = read_temp()
    print(f"temp: {temperature:.2f} C")

    # general check for if server is up
    server_up = False

    for port in devices["server"]["ports"]:
        if check_host(devices["server"]["ip"], port):
            server_up = True
            break
        else:
            server_up = False

    # check for if pc is up
    if check_host(devices["pc"]["ip"], devices["pc"]["ports"][0]):
        print(f"Host: {devices['pc']['ip']} is up")
        devices["pc"]["green"].value(1)
        devices["pc"]["red"].value(0)
    else:
        print(f"Host: {devices['pc']['ip']} is down or unreachable.")
        devices["pc"]["green"].value(0)
        devices["pc"]["red"].value(1)

    if server_up:
        print(f"Host: {devices['server']['ip']} is up")
        devices["server"]["green"].value(1)
        devices["server"]["red"].value(0)

        # check for jellyfin service
        if check_host(devices["server_jellyfin"]["ip"], devices["server_jellyfin"]["ports"][0]):
            print(f"Jellyfin on host: {devices['server_jellyfin']['ip']} is up")
            devices["server_jellyfin"]["green"].value(1)
            devices["server_jellyfin"]["red"].value(0)
        else:
            print(f"Jellyfin on host: {devices['server_jellyfin']['ip']} is down or unreachable.")
            devices["server_jellyfin"]["green"].value(0)
            devices["server_jellyfin"]["red"].value(1)

        if check_host(devices["server_web"]["ip"], devices["server_web"]["ports"][0]):
            print(f"Webpage on host: {devices['server_web']['ip']} is up")
            devices["server_web"]["green"].value(1)
            devices["server_web"]["red"].value(0)
        else:
            print(f"Webpage on host: {devices['server_web']['ip']} is down or unreachable.")
            devices["server_web"]["green"].value(0)
            devices["server_web"]["red"].value(1)
    else:
        print(f"Host: {devices['server']['ip']} is down or unreachable.")
        devices["server"]["green"].value(0)
        devices["server"]["red"].value(1)

        devices["server_jellyfin"]["green"].value(0)
        devices["server_jellyfin"]["red"].value(1)

        devices["server_web"]["green"].value(0)
        devices["server_web"]["red"].value(1)

    time.sleep(UPDATE_INTERVAL)
