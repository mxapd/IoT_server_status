import uasyncio
from machine import Pin, ADC

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


async def blink_led(pin, on_time, off_time):
    while True:
        pin.value(1)
        await uasyncio.sleep(on_time)
        pin.value(0)
        await uasyncio.sleep(off_time)


async def critical_blink(pin):
    while True:
        # Triple blink pattern
        for _ in range(3):
            pin.value(1)
            await uasyncio.sleep(0.2)
            pin.value(0)
            await uasyncio.sleep(0.2)
        # Pause between sequences
        await uasyncio.sleep(1.0)


def read_temp():
    tempsens = ADC(Pin(26))
    reading = tempsens.read_u16()
    voltage = reading * 3.3 / 65535  # convert to voltage (0-3.3V)
    temp_c = (voltage - 0.5) * 100  # convert voltage to temperature in °C
    # print(f"Raw: {tempsens}, Voltage: {voltage} V, Temp: {temp_c} °C")
    return temp_c


# INITIALIZE ALL LIGTS OFF
def initialize_lights_off(devices):
    for device in devices.values():
        for color in ["red", "green", "yellow"]:
            if color in device:
                device[color].value(0)
