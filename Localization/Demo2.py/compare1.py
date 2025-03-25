import json
from collections import defaultdict

clustered_results = []

def cluster_data(data, TIME_WINDOW):
    # Define time window (seconds)

    # Find the latest timestamp in the dataset
    all_timestamps = [entry.get("Timestamp") for entry in data if entry.get("Timestamp") is not None]
    latest_timestamp = max(all_timestamps) if all_timestamps else None

    # Filter data within the time window
    if latest_timestamp:
        data = [entry for entry in data if entry.get("Timestamp") and (latest_timestamp - entry["Timestamp"] <= TIME_WINDOW)]

    # Dictionary to store grouped entries
    grouped_data = defaultdict(list)

    # Group entries by Device_Name
    for entry in data:
        grouped_data[entry["Device_Name"]].append(entry)

    # Process each group
    clustered_results_window = []
    for device_name, entries in grouped_data.items():
        mac = list(set(entry["MAC"] for entry in entries))  # Collect all unique MACs
        features = entries[0]["Features"]
        
        # Extract all RSSI values, handling missing keys
        rssi_values = [entry.get("Average_RSSI", entry.get("RSSI")) for entry in entries if entry.get("Average_RSSI", entry.get("RSSI")) is not None]
        
        # Compute average RSSI if values exist
        avg_rssi = sum(rssi_values) / len(rssi_values) if rssi_values else None

        # Find first and last timestamps
        timestamps = [entry.get("Timestamp") for entry in entries if entry.get("Timestamp") is not None]
        first_timestamp = min(timestamps) if timestamps else None
        last_timestamp = max(timestamps) if timestamps else None

        # Determine SSID (use non-hidden if available)
        ssid = "<Hidden SSID>"
        for entry in entries:
            if entry.get("SSID") and entry["SSID"] != "<Hidden SSID>":
                ssid = entry["SSID"]
                break  # Stop at the first valid SSID

        # Create new JSON entry
        clustered_results_window.append({
            "Device_Name": device_name,
            "MAC": mac,
            "SSID": ssid,
            "Average_RSSI": avg_rssi,
            "First_Timestamp": first_timestamp,
            "Last_Timestamp": last_timestamp,
            "Features": features
        })
    print(clustered_results_window)

    # Extract existing device names for quick lookup
    existing_device_names = {entry["Device_Name"] for entry in clustered_results}
    
    # Filter new entries to avoid duplicates
    new_entries = [
        entry for entry in clustered_results_window if entry["Device_Name"] not in existing_device_names
    ]
    print(f"Found {len(new_entries)} new entries to append")
    
    # Append only new entries
    if new_entries:
        clustered_results.extend(new_entries)

        # Save updated data back to JSON
        with open("probe_request_results_clustered.json", "w") as outfile:
            json.dump(clustered_results, outfile, indent=4)
    
    print(f"Clustering complete. Processed last {TIME_WINDOW} seconds of data. Output saved to probe_request_results_clustered.json")
    return clustered_results