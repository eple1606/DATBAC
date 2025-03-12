import math
import json
import numpy as np
import matplotlib.pyplot as plt

# Load clustered data from JSON
with open("probe_request_results_clustered.json", "r") as file:
    data = json.load(file)

# Function to calculate distance from RSSI
def calculate_distance(rssi, A=-50, n=2):
    return 10 ** ((A - rssi) / (10 * n))

# Process devices
device_names = []
distances = []

for device in data:
    device_name = device["Device_Name"]
    rssi = device["Average_RSSI"]
    distance = calculate_distance(rssi)

    device_names.append(device_name)
    distances.append(distance)

# Create Radar Plot (Straight Line Representation)
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
ax.set_theta_zero_location('N')  # Devices will be placed along 0° (North)
ax.set_theta_direction(-1)  # Clockwise rotation
ax.set_title("Estimated Distance Radar", fontsize=14, fontweight='bold')

# Set all angles to 0 (North)
angles = np.zeros(len(distances))

# Plot device distances in a straight line
ax.scatter(angles, distances, color='red', s=100, label="Devices", alpha=0.75)

# Add labels for each device
for i, name in enumerate(device_names):
    ax.text(angles[i], distances[i] + 0.5, name, fontsize=10, ha='center', va='bottom', color='black')

# Adjust grid
ax.set_yticklabels([])  # Hide radial labels
ax.set_xticklabels(["N", "", "", "", "", "", "", ""], fontsize=10)  # Only show 'N'

# Show Radar Plot
plt.legend()
plt.show()
