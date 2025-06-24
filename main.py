from machine import Pin
import time
from secrets import WIFI_SSID, WIFI_PASSWORD
from lib import connect_wifi, check_host


red = Pin(2, Pin.OUT)
green = Pin(3, Pin.OUT)
yellow = Pin(4, Pin.OUT)

yellow.value(0)
red.value(0)
green.value(0)

if connect_wifi(WIFI_SSID, WIFI_PASSWORD) == 0:
    green.value(1)
    time.sleep(2)
    green.value(0)
else:
    red.value(1)
    time.sleep(2)
    red.value(0)
    raise RuntimeError("Failed to establish network connection")

while True:
    host_ip = "192.168.1.251"
    port = 80

    if check_host(host_ip, 80):
        print(f"Host: {host_ip} is up")
        red.value(0)
        green.value(1)
    else:
        green.value(0)
        red.value(1)
        print(f"Host: {host_ip} is down or unreachable.")

    time.sleep(60)

#i = 0

#while True:
#    i += 1
#    if i > 10:
#        break
#    green.value(1)  # ON
#    time.sleep(0.5)
#    green.value(0)  # OFF
#    time.sleep(0.5)
#
#    yellow.value(1)  # ON
#    time.sleep(0.5)
#    yellow.value(0)  # OFF
#    time.sleep(0.5)
#
#    red.value(1)  # ON
#    time.sleep(0.5)
#    red.value(0)  # OFF
#    time.sleep(0.5)
