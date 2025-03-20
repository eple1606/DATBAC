import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance
import time

max_distance=10 # Maximum display range in meters

def visualize_radar(data, ax, time_window=60):
    device_names = []
    rssi_values = []
    distances = []
    alphas = []
    labels = []
    current_time = time.time()
    
    for device in data:
        print(device)
        device_name = device["Device_Name"]
        first_timestamp = device["First_Timestamp"]
        rssi = device["Average_RSSI"]
        distance = calculate_distance(rssi)

        # Limit distance to the max range
        if distance > max_distance:
            continue

        age = current_time - first_timestamp
        alpha = max(0.2, 1 - (age / time_window))  # Fading effect
        print(alpha)

        alphas.append(alpha)
        labels.append(f"{device_name} / {rssi:.2f}dBm / {distance:.2f}m")
        device_names.append(device_name)
        rssi_values.append(rssi)
        distances.append(distance)

    angles = np.zeros(len(distances))  # Keep all devices aligned to North

    # Plot devices with scaled sizes
    ax.scatter(angles, distances, color='red', label="Devices", alpha=0.75)
    # Add labels for each device
    for i, name in enumerate(device_names):
        ax.text(angles[i], distances[i] + 0.3,labels[i], 
                fontsize=8, ha='center', va='bottom', color='black', 
                bbox=dict(facecolor='white', alpha=0.5))  # Background for readability
    # Set plot limits
    ax.set_ylim(0, max_distance)  # Max display range
    ax.set_xticks([])  # Hide x-axis labels
    ax.set_yticks(np.arange(0, max_distance + 1, 2))  # Y-axis every 2m
    ax.set_ylabel("Distance (m)")
    # Refresh the plot
    plt.legend()
    plt.draw()
    plt.pause(0.1)
