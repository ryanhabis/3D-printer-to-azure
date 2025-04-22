
from azure.iot.device import IoTHubDeviceClient
import requests
import time

# Azure IoT Hub Settings
CONNECTION_STRING = "[PASTE_DEVICE_CONNECTION_STRING_HERE]"
# OctoPrint Settings
OCTOPRINT_API_KEY = "[PASTE_OCTOPRINT_API_KEY_HERE]"
OCTOPRINT_URL = "http://localhost/api/printer"

# Initialize Azure client
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def get_printer_status():
    headers = {"X-Api-Key": OCTOPRINT_API_KEY}
    try:
        response = requests.get(OCTOPRINT_URL, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

while True:
    status = get_printer_status()
    if status:
        device_client.send_message(str(status))
        print(f"Sent to Azure: {status}")
    time.sleep(30)  # Send every 30 seconds
