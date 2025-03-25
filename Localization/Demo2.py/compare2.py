import json
from collections import defaultdict

clustered_results = []

def cluster_data(data, TIME_WINDOW):
    # Find the latest timestamp in the dataset
    all_timestamps = [entry.get("Timestamp") for entry in data if entry.get("Timestamp") is not None]
    latest_timestamp = max(all_timestamps) if all_timestamps else None
    print("Clustering: First fail")
    if not latest_timestamp:
        return clustered_results  # No valid timestamps, nothing to process
    print("Clustering: Second fail")
    # Filter data within the time window
    data = [entry for entry in data if latest_timestamp - entry["Timestamp"] <= TIME_WINDOW]
    print("Clustering: Third fail")
    # Dictionary to quickly find devices in clustered_results
    device_map = {entry["Device_Name"]: entry for entry in clustered_results}
    print("Clustering: Fourth fail")
    # Temporary storage for newly processed results
    new_clustered_results = {}

    for entry in data:
        device_name = entry["Device_Name"]
        mac = entry["MAC"]
        timestamp = entry["Timestamp"]
        rssi = entry.get("Average_RSSI", entry.get("RSSI"))
        features = entry["Features"]
        ssid = entry.get("SSID", "<Hidden SSID>")
        print("Clustering Loop: First fail")
        # Use an existing entry or create a new one
        if device_name in device_map:
            device_entry = device_map[device_name]
        else:
            device_entry = {
                "Device_Name": device_name,
                "MAC": set(),
                "SSID": "<Hidden SSID>",
                "Average_RSSI": None,
                "First_Timestamp": timestamp,
                "Last_Timestamp": timestamp,
                "Features": features,
                "RSSI_Values": []  # Temporary list for averaging RSSI
            }
        print("Clustering Loop: Second fail")
        # Update timestamps
        print(timestamp)
        device_entry["First_Timestamp"] = min(device_entry["First_Timestamp"], timestamp)
        device_entry["Last_Timestamp"] = max(device_entry["Last_Timestamp"], timestamp)

        # Store all unique MACs
        device_entry["MAC"].add(mac)
        print("Clustering Loop: Third fail")
        # Determine SSID (keep first non-hidden SSID)
        if ssid != "<Hidden SSID>":
            device_entry["SSID"] = ssid

        # Store RSSI values for averaging
        if rssi is not None:
            device_entry["RSSI_Values"].append(rssi)
        print("Clustering Loop: Fourth fail")
        # Save back to new_clustered_results
        new_clustered_results[device_name] = device_entry

    # Convert MAC sets to lists and calculate Average RSSI
    clustered_results.clear()
    for device in new_clustered_results.values():
        device["MAC"] = list(device["MAC"])
        device["Average_RSSI"] = sum(device["RSSI_Values"]) / len(device["RSSI_Values"]) if device["RSSI_Values"] else None
        del device["RSSI_Values"]  # Remove temporary list
        clustered_results.append(device)
    print("Clustering: Fifth fail")
    # Save updated data back to JSON
    with open("probe_request_results_clustered.json", "w") as outfile:
        json.dump(clustered_results, outfile, indent=4)

    print(f"Clustering complete. Processed last {TIME_WINDOW} seconds of data. Output saved to probe_request_results_clustered.json")
    return clustered_results
