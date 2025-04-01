import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance
import time

max_distance = 100  # Maximum display range in meters
valid_data = []

def visualize_plot(data, time_window=60):
    current_time = time.time()
    
    device_indices = {}  # Map device names to unique indices
    device_latest_data = {}  # Track the latest data entry for each device
    legend_labels = []
    device_counter = 1  # Start numbering devices from 1
    
    for device in data:
        device_name = device["Device_Name"]
        first_timestamp = device["First_Timestamp"]
        latest_timestamp = device["Last_Timestamp"]
        rssi = device["Average_RSSI"]
        distance = calculate_distance(rssi)

        # Assign a unique index to each device
        if device_name not in device_indices:
            device_indices[device_name] = device_counter
            device_counter += 1  # Increment for the next unique device
        
        device_index = device_indices[device_name]
        entry = (device_index, device_name, first_timestamp, latest_timestamp, rssi, distance)
        valid_data.append(entry)
        
        # Keep track of the latest timestamp for each device
        if device_name not in device_latest_data or latest_timestamp > device_latest_data[device_name][3]:
            device_latest_data[device_name] = entry
    
    # Sort by timestamp within each device group
    valid_data.sort(key=lambda x: x[2])  # x[2] = first_timestamp
    
    plt.clf()

    # Plotting
    for device_index, device_name, first_timestamp, latest_timestamp, rssi, distance in valid_data:
        # Show label only for the most recent entry of each device
        if device_latest_data[device_name] == (device_index, device_name, first_timestamp, latest_timestamp, rssi, distance): # Most Recent Device
            red = (1, 0, 0, 1)  # Bright red
            plt.scatter(device_index, distance, color=red)
            plt.text(device_index, distance + 0.2, 
                     f"{device_name} / {rssi:.2f}dBm / {distance:.2f}m", 
                     fontsize=8)
            #legend_labels.append(f"{device_name} / {rssi:.2f}dBm / {distance:.2f}m")

        else:
            age = current_time - first_timestamp
            alpha = max(0.05, 0.3 - (age / 300) * (0.3 - 0.05))
            color = (1, 0, 0, alpha)
            plt.scatter(device_index, distance, color=color)
        
    plt.legend(legend_labels)
    plt.ylim(0, max_distance)
    
    plt.xlabel("Device Nr.")
    plt.ylabel("Distance (m)")
    plt.title("Device Distance Visualization")
    plt.pause(0.5)
    plt.show()
