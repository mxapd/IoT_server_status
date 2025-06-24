from machine import Pin
import time
from secrets import WIFI_SSID, WIFI_PASSWORD
from lib import connect_wifi, check_host


red0 = Pin(2, Pin.OUT)
green0 = Pin(3, Pin.OUT)
yellow0 = Pin(4, Pin.OUT)

yellow0.value(0)
red0.value(0)
green0.value(0)

red1 = Pin(6, Pin.OUT)
green1 = Pin(7, Pin.OUT)
yellow1 = Pin(8, Pin.OUT)

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
    if check_host("192.168.1.251", 80):
        print("Host: 192.168.1.251 is up")
        red0.value(0)
        green0.value(1)
    else:
        green0.value(0)
        red0.value(1)
        print("Host: 192.168.1.251 is down or unreachable.")

    if check_host("192.168.1.208", 22):
        print("Host: 192.168.1.208 is up")
        red1.value(0)
        green1.value(1)
    else:
        green1.value(0)
        red1.value(1)
        print("Host: 192.168.1.208 is down or unreachable.")

    time.sleep(60)
