import json
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

def cluster_devices_by_rssi(input_file="probe_request_results.json", output_file="final_results.json", n_clusters=3):
    """
    Reads labeled device data from a JSON file, computes the average RSSI per device, 
    clusters the devices, and writes the results to a new JSON file.

    Args:
        input_file (str): Path to the JSON file containing probe request results.
        output_file (str): Path to save the clustered results.
        n_clusters (int): Number of clusters for KMeans.
    """
    # Step 1: Load device data
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[!] Error: Could not read probe request data.")
        return

    if not data:
        print("[!] No data available for clustering.")
        return

    # Step 2: Aggregate RSSI readings by device name
    rssi_data = defaultdict(list)
    for entry in data:
        rssi_data[entry["Device_Name"]].append(entry["RSSI"])

    # Step 3: Compute the average RSSI per device
    avg_rssi_per_device = {device: np.mean(rssi) for device, rssi in rssi_data.items()}

    # Step 4: Prepare data for clustering
    device_names = list(avg_rssi_per_device.keys())
    rssi_values = np.array(list(avg_rssi_per_device.values())).reshape(-1, 1)

    # Step 5: Apply KMeans clustering
    if len(rssi_values) < n_clusters:
        print("[!] Not enough devices for the desired clusters. Adjusting cluster count.")
        n_clusters = max(1, len(rssi_values))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(rssi_values)

    # Step 6: Update data with average RSSI and cluster labels
    clustered_data = []
    for entry in data:
        device_name = entry["Device_Name"]
        if device_name in avg_rssi_per_device:
            entry["RSSI"] = avg_rssi_per_device[device_name]  # Replace RSSI with Average RSSI
            entry["Cluster_Label"] = int(labels[device_names.index(device_name)])  # Assign cluster
            clustered_data.append(entry)

    # Step 7: Save the clustered data to the output JSON file
    with open(output_file, "w") as file:
        json.dump(clustered_data, file, indent=4)

    print(f"[*] Clustering complete! Results saved to '{output_file}'.")

