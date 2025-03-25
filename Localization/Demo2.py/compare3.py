import json
from collections import defaultdict

def cluster_data(data, TIME_WINDOW):
    global clustered_results
    
    # Convert clustered_results into a dictionary for efficient lookup
    device_dict = {entry["Device_Name"]: entry for entry in clustered_results}
    
    for entry in data:
        device_name = entry["Device_Name"]
        mac = entry["MAC"]
        ssid = entry["SSID"]
        rssi = entry["RSSI"]
        timestamp = entry["Timestamp"]
        features = entry["Features"]
        
        if device_name in device_dict:
            # Update existing entry
            device_entry = device_dict[device_name]
            
            # Add new MAC address if not present
            if mac not in device_entry["MAC"]:
                device_entry["MAC"].append(mac)
                
            # Update SSID (optional: keep the latest SSID or most frequent one)
            device_entry["SSID"] = ssid
            
            # Update timestamps and filter out old ones
            device_entry["Timestamps"].append((timestamp, rssi))
            device_entry["Timestamps"] = [t for t in device_entry["Timestamps"] if t[0] >= timestamp - TIME_WINDOW]
            
            # Recalculate average RSSI
            device_entry["Average_RSSI"] = sum(r for _, r in device_entry["Timestamps"]) / len(device_entry["Timestamps"])
            
            # Update first and last timestamps
            device_entry["First_Timestamp"] = min(t[0] for t in device_entry["Timestamps"])
            device_entry["Last_Timestamp"] = max(t[0] for t in device_entry["Timestamps"])
            
            # Merge features if needed
            device_entry["Features"] = features  # This could be modified to merge feature sets
        
        else:
            # Create a new entry if the device is not in the list
            device_dict[device_name] = {
                "Device_Name": device_name,
                "MAC": [mac],
                "SSID": ssid,
                "Average_RSSI": rssi,
                "First_Timestamp": timestamp,
                "Last_Timestamp": timestamp,
                "Features": features,
                "Timestamps": [(timestamp, rssi)],  # Internal list to track timestamps and RSSIs
            }
    
    # Convert back to list
    clustered_results = list(device_dict.values())
    
    return clustered_results