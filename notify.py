# server_notify_bridge.py
from pydbus import SessionBus
from gi.repository import GLib
import requests

PICO_IP = 'http://192.168.1.x/notify'  # Replace with your Pico's IP

def on_notification(app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout):
    print(f"Notification from {app_name}: {summary} - {body}")
    try:
        requests.post(PICO_IP, json={"app": app_name, "summary": summary, "body": body})
    except Exception as e:
        print("Failed to send to Pico:", e)

bus = SessionBus()
notifications = bus.get('org.freedesktop.Notifications')
notifications.onNotify = on_notification

print("Listening for notifications...")
loop = GLib.MainLoop()
loop.run()
