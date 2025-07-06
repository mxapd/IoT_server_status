from secrets import WIFI_SSID, WIFI_PASSWORD
from webserver import init_listener, update_temperature, handle_request
from wifi import connect_wifi, check_host
from hardware import read_temp, initialize_lights_off, devices

import uasyncio
import time
import gc 

UPDATE_INTERVAL = 60

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
        print(f"Free memory: {gc.mem_free()} bytes")
        print(f"Allocated: {gc.mem_alloc()} bytes")
        gc.collect()

uasyncio.run(main())
