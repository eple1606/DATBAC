import time
import json
from capture import start_sniffing, probe_data
from feature_extraction import extract_features
from anomaly_detection import detect_anomalies
import asyncio

# Dictionary to store device signatures and their assigned names
device_signatures = {}
device_counter = 1


def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    """
    global device_counter
    
    if device_signature not in device_signatures:
        # If this device signature doesn't exist, assign a new name (e.g., "Device 1")
        device_name = f"Device {device_counter}"
        device_signatures[device_signature] = device_name
        device_counter += 1
    else:
        # If this device signature already exists, return the existing name
        device_name = device_signatures[device_signature]
    
    return device_name


async def main():
    # Step 1: Start sniffing and capture probe requests for x seconds
    # Wait for the sniffing process to complete (30 seconds)
    print("[*] Capturing data for 30 seconds...")
    duration = 12  # Capture duration in seconds
    task = asyncio.create_task(start_sniffing(duration, interface="wlan0"))  # Replace with your Wi-Fi interface
    
    print("[*] Capturing data...")

    # Step 2: Feature extraction
    print("[*] Extracting features from captured probe requests...")
    print("Captured Probe Data:", probe_data)
    X, df = extract_features(probe_data)

    # Step 3: Anomaly detection
    print("[*] Detecting anomalies in the captured data...")
    detect_anomalies(X, df)

    # Step 4: Assign device names based on device signatures (e.g., SSID, RSSI, Probe Interval)
    print("[*] Assigning device names...")
    
    # Structure the data into a list of dictionaries suitable for JSON
    json_data = []

    for entry in probe_data:
        # Create a device signature based on SSID and other features like RSSI, Probe Interval, etc.
        device_signature = (entry["SSID"], entry["RSSI"], entry["Features"])

        # Get or assign a device name based on the device signature
        device_name = get_device_name(device_signature)

        # Add the device name to the entry
        json_entry = {
            "Device_Name": device_name,
            "MAC": entry["MAC"],
            "SSID": entry["SSID"],
            "RSSI": entry["RSSI"],
            "Timestamp": entry["Timestamp"],
            "Features": entry["Features"]
        }
        json_data.append(json_entry)

    # Step 5: Save captured data to a JSON file
    print("[*] Saving captured data to 'probe_request_results.json'...")

    with open("probe_request_results.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("[*] Data saved to 'probe_request_results.json'")
    
    await asyncio.sleep(5)  # Wait for 5 seconds

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("[*] Sniffing task cancelled")

if __name__ == "__main__":
    asyncio.run(main())
