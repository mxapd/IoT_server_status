from machine import Pin, ADC
import network
import time
import socket


def read_temp():
    tempsens = ADC(Pin(26))
    reading = tempsens.read_u16()
    voltage = reading * 3.3 / 65535  # convert to voltage (0-3.3V)
    temp_c = (voltage - 0.5) * 100  # convert voltage to temperature in °C
    # print(f"Raw: {tempsens}, Voltage: {voltage} V, Temp: {temp_c} °C")
    return temp_c


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
        return network_info


def check_host(host, port=22, timeout=1):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        print(f"{host} is reachable")
        return True
    except Exception as e:
        print(f"Cannot reach {host} Error: {e}")
        return False


# INITIALIZE ALL LIGTS OFF
def initialize_lights_off(devices):
    for device in devices.values():
        for color in ["red", "green", "yellow"]:
            if color in device:
                device[color].value(0)
