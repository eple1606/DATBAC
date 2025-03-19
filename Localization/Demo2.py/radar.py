import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance

def visualize_radar(data, ax, max_distance=10):
    device_names = []
    distances = []
    sizes = []  # Store sizes for scaling points

    for device in data:
        device_name = device["Device_Name"]
        rssi = device["Average_RSSI"]
        distance = calculate_distance(rssi)

        # Limit distance to the max range
        if distance > max_distance:
            continue

        device_names.append(device_name)
        distances.append(distance)

        # Scale size based on distance (closer devices appear larger)
        sizes.append(max(20, 200 - distance * 15))  # Min size 20, max ~200

    angles = np.zeros(len(distances))  # Keep all devices aligned to North

    # Plot devices with scaled sizes
    ax.scatter(angles, distances, color='red', s=sizes, label="Devices", alpha=0.75)

    # Add labels for each device
    for i, name in enumerate(device_names):
        ax.text(angles[i], distances[i] + 0.3, f"{name} {distances[i]:.2f}m", 
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
