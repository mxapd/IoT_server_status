from machine import Pin
import time
from secrets import WIFI_SSID, WIFI_PASSWORD
from lib import connect_wifi, check_host

# server
red0 = Pin(2, Pin.OUT)
green0 = Pin(3, Pin.OUT)
yellow0 = Pin(4, Pin.OUT)

yellow0.value(0)
red0.value(0)
green0.value(0)

# server jellyfin
red2 = Pin(11, Pin.OUT)
green2 = Pin(10, Pin.OUT)

# server web
red3 = Pin(15, Pin.OUT)
green3 = Pin(14, Pin.OUT)

# pc
red1 = Pin(6, Pin.OUT)
green1 = Pin(7, Pin.OUT)
yellow1 = Pin(8, Pin.OUT)

yellow1.value(0)
red1.value(0)
green1.value(0)


if connect_wifi(WIFI_SSID, WIFI_PASSWORD) == 0:
    green0.value(1)
    time.sleep(2)
    green0.value(0)
else:
    red0.value(1)
    time.sleep(2)
    red0.value(0)
    raise RuntimeError("Failed to establish network connection")

while True:
    # general check for if server is up
    if (check_host("192.168.1.251", 80)
        or check_host("192.168.1.251", 22)
            or check_host("192.168.1.251", 443)):
        print("Host: 192.168.1.251 is up")
        red0.value(0)
        green0.value(1)
    else:
        green0.value(0)
        red0.value(1)
        print("Host: 192.168.1.251 is down or unreachable.")

    # check for if pc is up
    if check_host("192.168.1.208", 22):
        print("Host: 192.168.1.208 is up")
        red1.value(0)
        green1.value(1)
    else:
        green1.value(0)
        red1.value(1)
        print("Host: 192.168.1.208 is down or unreachable.")

    # check for jellyfin service
    if check_host("192.168.1.251", 8096):
        print("Jellyfin on host: 192.168.1.251 is up")
        red2.value(0)
        green2.value(1)
    else:
        green2.value(0)
        red2.value(1)
        print("Jellyfin on host: 192.168.1.251 is down or unreachable.")

    # check for personal webpage
    if check_host("192.168.1.251", 80):
        print("Webpage on host: 192.168.1.208 is up")
        red3.value(0)
        green3.value(1)
    else:
        green3.value(0)
        red3.value(1)
        print("Webpage on host: 192.168.1.208 is down or unreachable.")

    time.sleep(60)
