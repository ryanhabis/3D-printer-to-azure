# OctoPrint-to-Azure Integration Guide  
_A complete walkthrough to connect your 3D printer to the cloud._  

---

## 🎯 **What You’ll Achieve**  
By the end of this guide, you’ll:  
1. Send printer telemetry (temperature, status) to Azure IoT Hub.  
2. (Optional) Upload G-code files to Azure Blob Storage.  
3. Monitor your printer remotely via Azure.  

---

## 🔧 **Prerequisites**  
- A working OctoPrint instance (on Raspberry Pi or PC).  
- An [Azure account](https://azure.microsoft.com/free/).  
- Basic terminal/Python knowledge.  

---

## Part 1: Azure Setup  

### 1.1 Create an Azure IoT Hub  
1. **Log in to the [Azure Portal](https://portal.azure.com/)**.  
2. Click **+ Create a resource** > **Internet of Things** > **IoT Hub**.  
3. Configure settings:  
   - **Subscription**: Choose your account.  
   - **Resource Group**: Create new (e.g., `OctoPrint-Cloud`).  
   - **Region**: Select the closest region (e.g., "East US").  
   - **IoT Hub Name**: `OctoPrint-Hub` (must be globally unique).  
4. Click **Review + Create**, then **Create**. Wait 2-3 minutes for deployment.  

### It should look like this.

![RS_Group Create](https://github.com/user-attachments/assets/101277ff-0ae3-4990-acbb-10417ef29ad2)

---

### 1.2 Register Your Printer as an IoT Device  
1. In your IoT Hub, go to **Explorers** > **IoT devices**.  
2. Click **+ Add Device**:  
   - **Device ID**: `octoprint-device` (lowercase, no spaces).  
   - **Authentication Type**: "Symmetric Key" (default).  
   - Check **Auto-generate keys**.  
3. Click **Save**.  
4. Copy the **Device Connection String** (click the device name > **Connection String**).  

This is what is should look like once you set up **azure IoT Hub** and the **Resource group**.

![RS_Group Create + IoT Hub](https://github.com/user-attachments/assets/3cb0a028-e3a5-4855-a8bf-d01336a535ca)

---

## Part 2: Configure OctoPrint  

### 2.1 Install the MQTT Plugin  
1. Open OctoPrint in your browser (usually `http://[YOUR_PI_IP]:5000`).  
2. Go to **Settings** (wrench icon) > **Plugin Manager** > **Get More**.  
3. Search for `MQTT`, then click **Install** on the "MQTT" plugin.  

**[MQTT plugin](plugins.octoprint.org/plugins/mqtt/)**

What the application looks like.

![MQTT example data](https://github.com/user-attachments/assets/5e941577-7b94-4e42-8230-28e9ff64bbb6)


### 2.2 Connect MQTT to Azure IoT Hub  
1. In OctoPrint, go to **Settings** > **MQTT**.  
2. Fill in the following:  
   - **Broker Host**: `[YourIoTHubName].azure-devices.net`  
     (Replace `[YourIoTHubName]` with your IoT Hub name, e.g., `OctoPrint-Hub.azure-devices.net`).  
   - **Port**: `8883` (TLS required).  
   - **Username**: `[YourIoTHubName].azure-devices.net/octoprint-device/?api-version=2021-04-12`  
     (Replace `[YourIoTHubName]` with your hub name).  
   - **Password**: Paste the **Device Connection String** from Part 1.2.  
   - **Publish Topic**: `devices/octoprint-device/messages/events/`  
3. Click **Save**.  

### 2.3 Enable OctoPrint API  
1. In OctoPrint, go to **Settings** > **API**.  
2. Copy the **API Key** (click "Generate New Key" if needed).  

---

## Part 3: Send Data to Azure  

### 3.1 Create a Python Script for Telemetry  
1. **SSH into your OctoPrint server** (e.g., Raspberry Pi).  
2. Install required packages:  
   ```bash
   pip install azure-iot-device requests
   ```
   
![installing iot device git](https://github.com/user-attachments/assets/0db53eda-8864-43d1-b421-c1442b1a7b0e)

   
3. Create a file `octo_to_azure.py`:  
   ```python
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
   ```  
4. Replace `[PASTE_...]` with your credentials.  
5. Run the script:  
   ```bash
   python3 octo_to_azure.py
   ```  

### 3.2 (Optional) Upload Files to Azure Blob Storage  
1. **Create a Storage Account** in Azure:  
   - Go to **Storage Accounts** > **+ Create**.  
   - Name: `octoprintstorage` (unique).  
   - **Redundancy**: "Locally-redundant storage (LRS)".  
2. **Create a Container**:  
   - Go to **Containers** > **+ Container**.  
   - Name: `gcode-files` (set access to "Blob").  
3. **Install Storage SDK**:  
   ```bash
   pip install azure-storage-blob
   ```  
4. Use this script to upload files:  
   ```python
   from azure.storage.blob import BlobServiceClient
   import os

   STORAGE_CONNECTION_STRING = "[PASTE_STORAGE_CONNECTION_STRING]"
   CONTAINER_NAME = "gcode-files"

   # Initialize client
   blob_service = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
   container_client = blob_service.get_container_client(CONTAINER_NAME)

   def upload_gcode(file_path):
       blob_name = os.path.basename(file_path)
       with open(file_path, "rb") as data:
           container_client.upload_blob(name=blob_name, data=data)
       print(f"Uploaded {blob_name} to Azure!")

   # Example: Upload a file
   upload_gcode("~/my_print.gcode")
   ```  

---

## Part 4: Verify the Connection  

### 4.1 Monitor IoT Hub Messages  
1. Install **[Azure IoT Explorer](https://github.com/Azure/azure-iot-explorer/releases)** (desktop tool).  
2. Open IoT Explorer > **Add Connection String** (use your IoT Hub’s connection string).  
3. Go to **Telemetry** > Start monitoring. You should see messages like:  
   ```json
   {"temperature": {"bed": 60.3, "tool0": 205.1}, "state": "Printing"}
   ```  

### 4.2 Check Azure Blob Storage (Optional)  
1. In Azure Portal, go to **Storage Accounts** > **octoprintstorage** > **Containers** > **gcode-files**.  
2. Verify uploaded files appear here.  

---

## 🚨 **Troubleshooting**  
- **MQTT Connection Failed**:  
  - Ensure port `8883` is open on your network.  
  - Recheck the Device Connection String and MQTT topic format.  
- **Script Errors**:  
  - Run `pip install --upgrade azure-iot-device requests` to update libraries.  
  - Confirm OctoPrint’s API key has read permissions.  

---

## 🏁 **Next Steps**  
- Trigger Azure Functions when prints start/end ([example guide](https://learn.microsoft.com/en-us/azure/azure-functions)).  
- Build dashboards with [Azure Power BI](https://powerbi.microsoft.com/) for printer analytics.  

**Congratulations! Your 3D printer is now cloud-powered!** ⚡  
