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
