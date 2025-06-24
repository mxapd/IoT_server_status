from machine import Pin, idle
import time
import subprocess
import network
from secrets import WIFI_SSID, WIFI_PASSWORD


def connect_wifi(ssid, key):
    nets = network.wlan.scan()
    for net in nets:
        if net.ssid == ssid:
            print('Network found!')
            network.wlan.connect(net.ssid, auth=(net.sec, key), timeout=5000)

            while not network.wlan.isconnected():
                idle()  # save power while waiting

            print('WLAN connection succeeded!')
            break


# tries to ping an ip address
# returns 0 if it gets a response otherwise returns 1
def ping(host):
    command = ['ping', '-c', '1', host]
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"{host} reachable: {result.stdout}")
        return 0
    else:
        print(f"Cannot reach {host}: {result.stderr}")
        return 1


red = Pin(2, Pin.OUT)
green = Pin(3, Pin.OUT)
yellow = Pin(4, Pin.OUT)

connect_wifi(WIFI_PASSWORD, WIFI_PASSWORD)

ping('192.168.1.251')


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
