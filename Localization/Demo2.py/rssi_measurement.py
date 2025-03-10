import numpy as np
import pandas as pd
import json

def calculate_average_rssi_from_json(json_file):
    """
    Calculates the average RSSI for each device grouped by 'Device_Name' from a JSON file.
    
    :param json_file: Path to the JSON file with device data
    :return: Dictionary of average RSSI values for each device (Device_Name)
    """
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)
    
    # Group by 'Device_Name' and calculate the mean RSSI for each device
    average_rssi = df.groupby('Device_Name')['RSSI'].mean().to_dict()
    
    # Print the average RSSI for each device
    print("\nAverage RSSI for devices with the same label name:")
    for device_name, avg_rssi in average_rssi.items():
        print(f"{device_name} - Average RSSI: {avg_rssi:.2f} dBm")
    
    return average_rssi
