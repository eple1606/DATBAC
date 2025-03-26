import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance
import time

max_distance = 30  # Maximum display range in meters

def visualize_plot(data, time_window=60):
    current_time = time.time()
    
    valid_data = []
    
    for device in data:
        device_name = device["Device_Name"]
        first_timestamp = device["First_Timestamp"]
        rssi = device["Average_RSSI"]
        distance = calculate_distance(rssi)
        
        valid_data.append((device_name, first_timestamp, rssi, distance))
    
    # Sort by timestamp to keep older points at lower alpha
    valid_data.sort(key=lambda x: x[1])
    
    plt.clf()
    
    # Plotting
    for i, (device_name, first_timestamp, rssi, distance) in enumerate(valid_data):
        age = current_time - first_timestamp
        
        if age <= time_window:
            color = (1, 0, 0, 1)  # Bright red for recent devices
        else:
            alpha = max(0.05, 1 - (age / (time_window * 2)))  # More extreme fading for older devices
            color = (1, 0, 0, alpha)
        
        plt.scatter(i + 1, distance, color=color)
        plt.text(i + 1, distance + 0.2, f"{device_name} / {rssi:.2f}dBm / {distance:.2f}m", fontsize=8, alpha=color[3])
    
    # Set maximum distance for the y-axis (adjustable with max_distance variable)
    plt.ylim(0, max_distance)
    
    plt.xlabel("Device Nr.")
    plt.ylabel("Distance (m)")
    plt.title("Device Distance Visualization")
    plt.pause(0.5)
    plt.show()
