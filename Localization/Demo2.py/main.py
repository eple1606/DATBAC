import time
import json
import asyncio
from capture import start_sniffing, probe_data
from feature_extraction import extract_features
from anomaly_detection import detect_anomalies
from distance_measurement import measure_distance_to_persistent_device  # Import the distance measurement logic


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


async def capture_data(duration, interface="wlan0"):
    """
    Captures probe request data asynchronously for the given duration.
    """
    print("[*] Starting to capture data asynchronously...")
    start_sniffing(duration, interface)
    await asyncio.sleep(duration)
    return probe_data


async def process_data(probe_data):
    """
    Processes captured data asynchronously, including feature extraction and anomaly detection.
    """
    print("[*] Extracting features from captured probe requests...")
    if probe_data == []:
        print("[*] No data captured. Exiting")
        return None
    X, df = extract_features(probe_data)

    print("[*] Detecting anomalies in the captured data...")
    df_filtered = detect_anomalies(X, df)
    return df_filtered


async def save_data(probe_data):
    """
    Saves the captured data to a JSON file asynchronously.
    """
    print("[*] Saving captured data to 'probe_request_results.json'...")
    json_data = []

    for entry in probe_data:
        device_signature = (entry["SSID"], entry["Features"])
        device_name = get_device_name(device_signature)

        json_entry = {
            "Device_Name": device_name,
            "MAC": entry["MAC"],
            "SSID": entry["SSID"],
            "RSSI": entry["RSSI"],
            "Timestamp": entry["Timestamp"],
            "Features": entry["Features"]
        }
        json_data.append(json_entry)

    with open("probe_request_results.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("[*] Data saved to 'probe_request_results.json'")


async def measure_distance(probe_data, df_filtered):
    """
    Measure the distance to persistent devices asynchronously.
    Instead of a known MAC, it will measure distance for all persistent devices.
    """
    print("[*] Measuring distance to persistent devices...")
    
    for index, row in df_filtered.iterrows():
        # Assuming that each device in df_filtered is persistent
        mac = row["MAC"]
        distance = await measure_distance_to_persistent_device(df_filtered, mac)
        
        if distance:
            print(f"Distance to persistent device {mac}: {distance:.2f} meters")
        else:
            print(f"Device with MAC address {mac} not found.")


async def main():
    duration = 30  # Duration for sniffing

    # Step 1: Capture data asynchronously
    print("[*] Capturing data for 30 seconds...")
    probe_data = await capture_data(duration=duration, interface="wlan0")

    # Step 2: Process data asynchronously (feature extraction + anomaly detection)
    df_filtered = await process_data(probe_data)

    # Step 3: Save captured data to a JSON file
    await save_data(probe_data)

    # Step 4: Measure distance to all persistent devices asynchronously
    await measure_distance(probe_data, df_filtered)

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
