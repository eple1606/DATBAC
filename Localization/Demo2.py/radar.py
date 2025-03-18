import math
import json
import numpy as np
import matplotlib.pyplot as plt
from distance_measurement import calculate_distance

def visualize_radar(data, ax):
    # Load clustered data from JSON
    #with open("probe_request_results_clustered.json", "r") as file:
    #    data = json.load(file)

    # Process devices
    device_names = []
    distances = []

    for device in data:
        device_name = device["Device_Name"]
        rssi = device["Average_RSSI"]
        distance = calculate_distance(rssi)

        device_names.append(device_name)
        distances.append(distance)

    # Set all angles to 0 (North)
    angles = np.zeros(len(distances))
    print(distances)
    # Plot device distances in a straight line
    ax.scatter(angles, distances, color='red', s=100, label="Devices", alpha=0.75)

    # Add labels for each device
    for i, name in enumerate(device_names):
        ax.text(angles[i], distances[i] + 0.5, name, fontsize=10, ha='center', va='bottom', color='black')

    # Show Radar Plot
    plt.legend()
    plt.draw()
    plt.pause(0.1)  # Allow GUI events to update

