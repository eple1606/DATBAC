import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance
import time

max_distance=100 # Maximum display range in meters

def visualize_plot(data, ax, time_window=60):
    device_names = []
    rssi_values = []
    distances = []
    alphas = []
    labels = []
    current_time = time.time()
    print("Radar: First fail")
    for device in data:
        print(device)
        device_name = device["Device_Name"]
        first_timestamp = device["First_Timestamp"]
        rssi = device["Average_RSSI"]
        print(rssi)
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
    print("Radar: Second fail")
    angles = np.zeros(len(distances))  # Keep all devices aligned to North
    
    ax.clear()
    print("clearing")

    ax.set_title("Estimated Distance Radar", fontsize=14, fontweight='bold')
    print("Radar: Third fail")
    # Adjust grid
    print("Radar: Fourth fail")
    # Plot devices with scaled sizes
    print(angles)
    print(distances)
    print(alphas)
    ax.scatter(angles, distances, color='red', label="Devices", alpha=alphas, s=100 * np.array(alphas))
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
    print("Radar: Fifth fail")
    # Add labels for each device
    for i, name in enumerate(device_names):
        ax.text(angles[i] - np.deg2rad(5),  # Shift left
                distances[i] + 2.5,
                labels[i], 
                fontsize=8, ha='right', va='center', color='black', 
                bbox=dict(facecolor='white', alpha=0.5))

    print("Radar: Sixth fail")
    # Set plot limits
    ax.set_ylim(0, max_distance)  # Max display range
    ax.set_xticks([])  # Hide x-axis labels
    ax.set_yticks(np.arange(0, max_distance + 1, 2))  # Y-axis every 2m
    ax.set_ylabel("Distance (m)")
    # Refresh the plot
    plt.draw()
    plt.pause(0.1)
