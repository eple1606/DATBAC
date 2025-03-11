import time
import json
from capture import start_sniffing, probe_data
from feature_extraction import extract_features
from anomaly_detection import detect_anomalies
from rssi_measurement import calculate_average_rssi  # Import the function to calculate average RSSI
from clustering import cluster_devices_by_rssi  # Import the clustering function from clustering.py


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

def main():
    # Step 1: Start sniffing and capture probe requests for x seconds
    print("[*] Capturing data for 30 seconds...")
    duration = 30  # Capture duration in seconds
    start_sniffing(duration, interface="wlan0")  # Replace with your Wi-Fi interface

    time.sleep(2)  # Wait for 2 seconds to ensure the sniffing process has finished

    # Step 2: Feature extraction
    print("[*] Extracting features from captured probe requests...")
    print("Captured Probe Data:", probe_data)
    X, df = extract_features(probe_data)

    # Step 3: Anomaly detection
    print("[*] Detecting anomalies in the captured data...")
    df_filtered = detect_anomalies(X, df)  # Filter out persistent devices

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

    # Step 6: Calculate average RSSI for known devices (persistent devices)
    print("[*] Calculating average RSSI for persistent devices...")
    average_rssi = calculate_average_rssi(df_filtered)  # Call the function to calculate average RSSI

    # Step 7: Cluster the devices based on their average RSSI values
    print("[*] Clustering devices by average RSSI...")
    clustered_devices = cluster_devices_by_rssi(average_rssi)  # Call clustering from clustering.py

    # Step 8: Replace the RSSI values with the average RSSI and prepare the data for final output
    print("[*] Replacing RSSI with average RSSI and preparing final clustered data...")

    # Updated data to be stored in the new JSON file
    final_json_data = []

    for cluster, devices in clustered_devices.items():
        for device in devices:
            # Find the original device data by MAC address
            device_data = next((entry for entry in json_data if entry["MAC"] == device["MAC"]), None)
            if device_data:
                # Replace the RSSI with the average RSSI
                device_data["RSSI"] = device["Average_RSSI"]

                # Add the cluster label to the device data
                device_data["Cluster_Label"] = cluster
                
                # Append to the final data list
                final_json_data.append(device_data)

    # Step 9: Save the final clustered and updated data to a new JSON file
    print("[*] Saving clustered and updated data to 'final_clustered_data.json'...")

    with open("final_clustered_data.json", "w") as json_file:
        json.dump(final_json_data, json_file, indent=4)

    print("[*] Clustered and updated data saved to 'final_clustered_data.json'")

if __name__ == "__main__":
    main()
