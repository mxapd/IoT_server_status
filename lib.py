import network
import time


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
        return 0
