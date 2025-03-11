import time
import json
from capture import start_sniffing, probe_data
from feature_extraction import extract_features
from anomaly_detection import detect_anomalies
from rssi_measurement import calculate_average_rssi  # (If still used elsewhere)
from clustering import cluster_devices_with_sliding_window  # Import our new clustering function

# Dictionary to store device signatures and their assigned names
device_signatures = {}
device_counter = 1

def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    """
    global device_counter
    
    if device_signature not in device_signatures:
        device_name = f"Device {device_counter}"
        device_signatures[device_signature] = device_name
        device_counter += 1
    else:
        device_name = device_signatures[device_signature]
    
    return device_name

def main():
    # Step 1: Start sniffing and capture probe requests for a duration
    print("[*] Capturing data for 30 seconds...")
    duration = 30  # Capture duration in seconds
    start_sniffing(duration, interface="wlan0")
    
    time.sleep(2)  # Wait to ensure the sniffing process has finished
    
    # Step 2: Feature extraction
    print("[*] Extracting features from captured probe requests...")
    print("Captured Probe Data:", probe_data)
    X, df = extract_features(probe_data)
    
    # Step 3: Anomaly detection
    print("[*] Detecting anomalies in the captured data...")
    df_filtered = detect_anomalies(X, df)  # Filter out persistent devices
    
    # Step 4: Assign device names based on device signatures
    print("[*] Assigning device names...")
    json_data = []
    for entry in probe_data:
        device_signature = (entry["SSID"], entry["RSSI"], entry["Features"])
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
    
    # Step 5: Save captured data to a JSON file
    print("[*] Saving captured data to 'probe_request_results.json'...")
    with open("probe_request_results.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("[*] Data saved to 'probe_request_results.json'")
    
    # Step 6: Cluster the devices using the sliding window method
    print("[*] Clustering devices based on the most recent signals...")
    cluster_devices_with_sliding_window(file_path="probe_request_results.json", output_path="final_clustered_data.json", window_size=10, n_clusters=3)

if __name__ == "__main__":
    main()
