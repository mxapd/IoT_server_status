import uasyncio
from hardware import blink_led, critical_blink

NOTIFICATION_PRIORITIES = {
    "none": 0,
    "info": 1,
    "warning": 2,
    "critical": 3
}

notification_tasks = {}
notification_states = {}
device_priority_levels = {}

async def handle_notification(device_name, notify_level):
    global notification_tasks, notification_states, device_priority_levels

    current_priority = device_priority_levels.get(device_name, 0)
    new_priority = NOTIFICATION_PRIORITIES.get(notify_level, 0)

    print(f"current: {current_priority}")
    print(f"new: {new_priority}")

    if notify_level == "none" or new_priority > current_priority:
        if device_name in notification_tasks and notification_tasks[device_name] is not None:
            notification_tasks[device_name].cancel()
            try:
                await notification_tasks[device_name]
            except uasyncio.CancelledError:
                pass

        device_priority_levels[device_name] = new_priority
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

        else:
            print(f"Notification ignored - Level: {notify_level} (priority {new_priority}) is lower than current level: {notification_states.get(device_name, 'none')} (priority {current_priority})")

