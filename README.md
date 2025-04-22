# 3D-printer-to-Azure Integration  
**Connect your 3D printer to Azure for cloud monitoring, automation, and analytics!**

This project enables you to connect OctoPrint (a 3D printer management tool) to Microsoft Azure. By doing this, you can:  
- Send real-time printer telemetry (temperature, status) to Azure IoT Hub.  
- Store G-code files in Azure Blob Storage.  
- Trigger serverless workflows in Azure Functions (e.g., alerts, post-processing).  

## ⚙️ **Prerequisites**  
1. A Raspberry Pi/computer running OctoPrint.  
2. An Azure account (free tier available).  
3. Basic familiarity with Python and Azure services.  

## 🚀 **Features**  
- **Real-time monitoring**: Track printer status from anywhere via Azure.  
- **Cloud backups**: Automatically upload prints to Azure Storage.  
- **Automation**: Run Azure Functions when prints start/finish.  

## 🔌 **What You’ll Use**  
- **Azure IoT Hub**: For device communication.  
- **Azure Blob Storage**: For file storage.  
- **OctoPrint API/MQTT**: To send data to Azure.  

---

**Follow the [Step-by-Step Guide](GUIDE.md) to set this up!**  
