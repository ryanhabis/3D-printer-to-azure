
# Step-by-Step Guide: OctoPrint to Azure  

## Part 1: Set Up Azure Services  

### 1.1 Create an Azure IoT Hub  
1. Log in to the [Azure Portal](https://portal.azure.com/).  
2. Search for **IoT Hub** and click **Create**.  
3. Fill in:  
   - **Subscription**: Your Azure subscription.  
   - **Resource Group**: Create new (e.g., `OctoPrint-Resources`).  
   - **Region**: Pick the closest to you.  
   - **IoT Hub Name**: e.g., `OctoPrint-Hub`.  
4. Click **Review + Create**, then **Create**.  

### 1.2 Register a Device in IoT Hub  
1. Go to your IoT Hub > **IoT devices** > **Add Device**.  
2. Name the device (e.g., `octoprint-pi`).  
3. Check **Auto-generate keys** and click **Save**.  
4. Copy the **Device Connection String** (under the device’s details).  

### 1.3 Create Azure Blob Storage (Optional)  
1. Search for **Storage Account** in Azure Portal and create one.  
2. Under **Containers**, create a new container named `gcode-files`.  
3. Copy the **Connection String** (under **Access Keys**).  

---

## Part 2: Configure OctoPrint  

### 2.1 Install the MQTT Plugin  
1. Open OctoPrint in your browser.  
2. Go to **Settings** > **Plugin Manager** > **Get More**.  
3. Search for `MQTT`, install the **MQTT Plugin**.  

### 2.2 Configure MQTT for Azure IoT Hub  
1. Go to **Settings** > **MQTT**.  
2. Configure as follows:  
   - **Broker Host**: `[YourIoTHub].azure-devices.net` (replace with your IoT Hub name).  
   - **Port**: `8883` (use TLS).  
   - **Username**: `[YourIoTHub].azure-devices.net/octoprint-pi/?api-version=2021-04-12`.  
   - **Password**: Paste the **Device Connection String** from Part 1.2.  
   - **Publish Topic**: `devices/octoprint-pi/messages/events/`.  
3. Click **Save**.  

### 2.3 Generate OctoPrint API Key  
1. Go to **Settings** > **API**.  
2. Copy the **API Key** (keep this secure!).  

---

## Part 3: Send Data to Azure  

### 3.1 Send Telemetry via Python Script  
1. SSH into your OctoPrint server (e.g., Raspberry Pi).  
2. Install the Azure IoT SDK:  
   ```bash
   pip install azure-iot-device
   ```  
3. Create a file `send_telemetry.py`:  
   ```python
   from azure.iot.device import IoTHubDeviceClient
   import requests
   import time

   # Azure IoT Hub Connection String
   CONNECTION_STRING = "[PASTE_DEVICE_CONNECTION_STRING]"
   # OctoPrint API Key
   API_KEY = "[PASTE_OCTOPRINT_API_KEY]"
   OCTOPRINT_URL = "http://localhost/api/printer"

   device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

   def get_printer_status():
       headers = {'X-Api-Key': API_KEY}
       response = requests.get(OCTOPRINT_URL, headers=headers)
       return response.json()

   while True:
       status = get_printer_status()
       device_client.send_message(str(status))
       print(f"Sent: {status}")
       time.sleep(60)  # Send every 60 seconds
   ```  
4. Run the script:  
   ```bash
   python3 send_telemetry.py
   ```  

### 3.2 Upload Files to Azure Storage (Optional)  
1. Install Azure Storage SDK:  
   ```bash
   pip install azure-storage-blob
   ```  
2. Use this script to upload G-code:  
   ```python
   from azure.storage.blob import BlobServiceClient
   import os

   CONNECTION_STRING = "[PASTE_STORAGE_CONNECTION_STRING]"
   CONTAINER_NAME = "gcode-files"

   blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
   container_client = blob_service.get_container_client(CONTAINER_NAME)

   def upload_to_azure(file_path):
       blob_name = os.path.basename(file_path)
       with open(file_path, "rb") as data:
           container_client.upload_blob(name=blob_name, data=data)
       print(f"Uploaded {blob_name} to Azure!")

   # Example: Upload a file when a print starts
   upload_to_azure("/path/to/your/file.gcode")
   ```  

---

## Part 4: Verify & Monitor  
- **IoT Hub**: Use **Azure IoT Explorer** (tool) to see incoming messages.  
- **Storage**: Check the `gcode-files` container in Azure Portal.  
- **OctoPrint**: Confirm the MQTT plugin shows a connected status.  

---

## 🛠️ **Troubleshooting**  
- **MQTT Errors**: Ensure port `8883` is open and credentials are correct.  
- **API Issues**: Check the OctoPrint API key and network connectivity.  
- **Azure SDK Errors**: Update packages with `pip install --upgrade azure-iot-device`.  

**Done! Your 3D printer is now cloud-connected!** 🌩️  
```

---

Let me know if you need adjustments (e.g., more details on security or specific Azure steps)! 🔧
