from machine import Pin
from secrets import WIFI_SSID, WIFI_PASSWORD
from lib import connect_wifi, check_host, read_temp, initialize_lights_off
from web import init_listener, check_listener_async, update_temperature
import uasyncio
import time

UPDATE_INTERVAL = 60

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

notification_tasks = {}
notification_states = {}

initialize_lights_off(devices)

connect_result = connect_wifi(WIFI_SSID, WIFI_PASSWORD)

if connect_result != 1:
    for _ in range(3):
        devices["server"]["green"].value(1)
        time.sleep(0.5)
        devices["server"]["green"].value(0)
        time.sleep(0.5)
    ip_addr = str(connect_result[0])
else:
    for _ in range(3):
        devices["server"]["red"].value(1)
        time.sleep(0.5)
        devices["server"]["red"].value(0)
        time.sleep(0.5)
        raise RuntimeError("Failed to establish network connection")

init_listener(ip_addr, 80)


async def main():
    monitor_task = uasyncio.create_task(monitor_hosts())
    request_task = uasyncio.create_task(handle_request())

    await uasyncio.gather(monitor_task, request_task)


async def monitor_hosts():
    while True:
        temperature = read_temp()
        print(f"temp: {temperature:.2f} C")
        update_temperature(temperature)


        # general check for if server is up
        server_up = False

        for port in devices["server"]["ports"]:
            if check_host(devices["server"]["ip"], port):
                server_up = True
                break

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

        await uasyncio.sleep(UPDATE_INTERVAL)


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


async def handle_notification(device_name, notify_level):
    global notification_tasks, notification_states

    if device_name in notification_tasks:
        notification_tasks[device_name].cancel()
        try:
            await notification_tasks[device_name]
        except uasyncio.CancelledError:
            pass

    notification_states[device_name] = notify_level

    if device_name in devices and "yellow" in devices[device_name]:
        yellow_pin = devices[device_name]["yellow"]

        if notify_level == "info":
            devices[device_name]["yellow"].value(1)
            notification_tasks[device_name] = None

        elif notify_level == "warning":
            task = uasyncio.create_task(blink_led(yellow_pin, 1.0, 1.0))
            notification_tasks[device_name] = task

        elif notify_level == "critical":
            task = uasyncio.create_task(critical_blink(yellow_pin))
            notification_tasks[device_name] = task

        elif notify_level == "none" or notify_level is None:
            yellow_pin.value(0)
            notification_tasks[device_name] = None

        print(f"Notification set - Level: {notify_level}, Device: {device_name}")


async def handle_request():
    while True:
        try:
            listener_result = await check_listener_async()

            if listener_result[0] == "get_request":
                await uasyncio.sleep(0.01)
                continue

            if listener_result[1] in ["info", "warning", "critical"]:

                device_name = listener_result[0]
                notify_level = listener_result[1]

                if device_name in devices:
                    await handle_notification(device_name, notify_level)
                    print(f"Notification received - Level: {notify_level}, From: {device_name}")

                else:
                    print(f"No such device: {device_name}")
            else:
                print(f"No such notify level: {listener_result[1]}")
            await uasyncio.sleep(0.01)
        except Exception as e:
            print(f"Error in handle_request: {e}")
            await uasyncio.sleep(0.1)

uasyncio.run(main())
