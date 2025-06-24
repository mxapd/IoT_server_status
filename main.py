# from machine import Pin
# #import time
import subprocess
# red = Pin(2, Pin.OUT)
# green = Pin(3, Pin.OUT)
# yellow = Pin(4, Pin.OUT)
# i = 0
#
# while True:
#     i += 1
#     if i > 10:
#         break
#     green.value(1)  # ON
#     time.sleep(0.5)
#     green.value(0)  # OFF
#     time.sleep(0.5)
#
#     yellow.value(1)  # ON
#     time.sleep(0.5)
#     yellow.value(0)  # OFF
#     time.sleep(0.5)
#
#     red.value(1)  # ON
#     time.sleep(0.5)
#     red.value(0)  # OFF
#     time.sleep(0.5)


def ping(host):
    command = ['ping', '-c', '1', host]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"{host} reachable: {result.stdout}")
        return 0
    else:
        print(f"Cannot reach {host}: {result.stderr}")
        return 1


ping('192.168.1.251')  # Replace with the desired IP address
