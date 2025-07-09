from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

PICO_IP = "192.168.1.116"
PICO_PORT = 80


def get_device_statuses():
    try:
        response = requests.get(f"http://{PICO_IP}:{PICO_PORT}/status", timeout=50)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching device statuses: {e}")
    return {}


def get_temperature():
    try:
        response = requests.get(f"http://{PICO_IP}:{PICO_PORT}/temperature", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return round(data.get("temperature", 0), 1), data.get("unit", "celsius")
    except Exception as e:
        print(f"Error fetching temperature: {e}")
    return None, None


def send_notification(device, level):
    try:
        payload = {"device": device, "notify": level}
        print(f"Sending payload: {payload}")

        # Convert to JSON string manually to ensure proper formatting
        import json
        json_payload = json.dumps(payload)
        print(f"JSON payload: {json_payload}")

        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(json_payload))
        }

        response = requests.post(
            f"http://{PICO_IP}:{PICO_PORT}/",
            data=json_payload,  # Use data instead of json parameter
            headers=headers,
            timeout=5
        )

        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")

        return response.status_code == 200

    except Exception as e:
        print(f"Error sending notification: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    message = ''
    if request.method == 'POST':
        device = request.form.get('device')
        level = request.form.get('level')
        if send_notification(device, level):
            message = f"Notification sent to {device} with level {level}"
        else:
            message = "Failed to send notification."

    temperature, unit = get_temperature()
    device_statuses = get_device_statuses()
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if temperature else "Unavailable"

    return render_template('dashboard.html',
                           temperature=temperature,
                           unit=unit,
                           last_update=last_update,
                           device_statuses=device_statuses,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
