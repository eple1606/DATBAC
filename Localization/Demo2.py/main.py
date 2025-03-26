import time
import json
from capture import start_sniffing, probe_data
from feature_extraction import extract_features
from anomaly_detection import detect_anomalies
import asyncio
from collections import defaultdict
from radar import visualize_radar  # Import radar visualization function
from clustering import cluster_data
import matplotlib.pyplot as plt
import keyboard
from device_signature import get_device_name
import os
from plot import visualize_plot


TIME_WINDOW = 60  # Time window in seconds

# List to store all clustered results
clustered_results_all = []

def on_click(event):
    print(f"Clicked at ({event.x}, {event.y})")


async def save_packets():
    while True:
        print("data_data_data_data_data_data_data_data_data_data_data")
        print(probe_data)
        # Step 2: Feature extraction
        print("[*] Extracting features from captured probe requests...")

        if not probe_data:
            print("[*] No probe data captured. Skipping this iteration.")
            await asyncio.sleep(1)
            continue

        X, df = extract_features(probe_data)

        # Step 3: Anomaly detection
        print("[*] Detecting anomalies in the captured data...")
        detect_anomalies(X, df)

        # Step 4: Assign device names based on device signatures (e.g., SSID, RSSI, Probe Interval)
        print("[*] Assigning device names...")
        
        # Structure the data into a list of dictionaries suitable for JSON
        json_data = []

        for entry in probe_data:
            # Create a device signature based on SSID and other features like RSSI, Probe Interval, etc.
            device_signature = (entry["SSID"], entry["MAC"], entry["Features"])

            # Get or assign a device name based on the device signature
            device_name = get_device_name(device_signature)

            # Add the device name to the entry
            json_entry = {
                "Device_Name": device_name,
                "MAC": entry["MAC"],
                "SSID": entry["SSID"],
                "RSSI": entry["RSSI"],
                "Timestamp": entry["Timestamp"],
                "Features": entry["Features"]
            }
            json_data.append(json_entry)

        # Step 5: Save captured data to a JSON file
        print("[*] Saving captured data to 'probe_request_results.json'...")
        
        with open("probe_request_results.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print("[*] Data saved to 'probe_request_results.json'")
        print("-----------------------------")
        print(json_data)
        print("-----------------------------")
        

        # Step 6: Cluster the data

        # Load JSON data
        #with open("probe_request_results.json", "r") as file:
        #   data = json.load(file)
        
        # Perform clustering
        print("[*] Clustering data...")
        clustered_results = cluster_data(json_data, TIME_WINDOW)
        
        # Step 7: Call radar visualization function
        print("Generating radar visualization...")
        print(clustered_results)
        #visualize_radar(clustered_results, ax)
        #print("[*] Radar visualization updated")
        visualize_plot(clustered_results)
        print("[*] Plot visualization updated")
        
        await asyncio.sleep(1)

async def main():
    # Check if the file exists
    if os.path.exists("probe_request_results_clustered.json"):
        # Rename the existing file to .bak
        os.rename("probe_request_results_clustered.json", "probe_request_results_clustered.json.bak")
        print("[*] Existing 'probe_request_results_clustered.json' renamed to 'probe_request_results_clustered.json.bak'")
    
    if os.path.exists("probe_request_results.json"):
        # Rename the existing file to .bak
        os.rename("probe_request_results.json", "probe_request_results.json.bak")
        print("[*] Existing 'probe_request_results.json' renamed to 'probe_request_results.json.bak'")


    '''
    # Create Radar Plot (Straight Line Representation)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.set_theta_zero_location('N')  # Devices will be placed along 0° (North)
    ax.set_theta_direction(-1)  # Clockwise rotation
    ax.set_title("Estimated Distance Radar", fontsize=14, fontweight='bold')

    # Adjust grid
    ax.set_xticks(ax.get_xticks())
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels([])  # Hide radial labels
    ax.set_xticklabels(["N", "", "", "", "", "", "", ""], fontsize=10)  # Only show 'N'
    ax.scatter(0, 1, color='red', s=100, label="Devices", alpha=0.75)
    fig.canvas.mpl_connect('button_press_event', on_click)
    '''
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')

    plt.ion()
    plt.draw()
    plt.show()

    # Step 1: Start sniffing and capture probe requests until you press 'esc'
    task1 = asyncio.create_task(start_sniffing(interface="wlan0"))  # Replace with your Wi-Fi interface
    time.sleep(3)
    task2 = asyncio.create_task(save_packets())
    print("[*] Capturing data...")

    while True:
        if keyboard.is_pressed('esc'):
            print("[*] Stopping the program...")
            break
        await asyncio.sleep(1)
    
    plt.ioff()
    task1.cancel()
    task2.cancel()
    try:
        await task1
    except asyncio.CancelledError:
        print("[*] Sniffing task cancelled")
    try:
        await task2
    except asyncio.CancelledError:
        print("[*] Saving task cancelled")

    print("[*] Program completed")
    
if __name__ == "__main__":
    asyncio.run(main())
