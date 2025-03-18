import math
import json

# Load clustered data from JSON
with open("probe_request_results_clustered.json", "r") as file:
    data = json.load(file)

# Function to calculate distance from RSSI free model
def calculate_distance(rssi, A=-50, n=2):
    """
    Estimate the distance to a device using RSSI.

    :param rssi: Received Signal Strength Indicator (RSSI) in dBm.
    :param A: RSSI at 1 meter distance (default is -50 dBm).
    :param n: Path loss exponent (default is 2 for free-space, but can vary).
    :return: Estimated distance in meters.
    """
    return 10 ** ((A - rssi) / (10 * n))

#free loss path model
def calculate_distance3(rssi, A=-50, n=3, X=0, d0=1, C = 0):
    """
    Calculate the distance to a device based on RSSI using the Path Loss model.

    :param rssi: Received Signal Strength Indicator (RSSI) in dBm.
    :param A: RSSI at reference distance (typically 1 meter, default is -50 dBm).
    :param n: Path loss exponent (default is 3 for tunnels).
    :param X: Shadowing effect (default is 0).
    :param d0: Reference distance (default is 1 meter).
    :param C: Environmental correction constant (default is 0).
    :return: Estimated distance in meters.
    """
    # Rearranged formula to calculate distance
    distance = d0 * 10 ** ((A - rssi - X + C) / (10 * n))
    return distance

# Function to measure the distance to a fingerprinted device
def measure_distance_to_device(data, device_name):
    """
    Measure the distance to a fingerprinted device using its Average RSSI.

    :param data: List of dictionaries containing fingerprinted device data.
    :param device_name: The Device_Name of the known device.
    :return: Estimated distance to the device.
    """
    # Search for the device by Device_Name
    device_entry = next((entry for entry in data if entry["Device_Name"] == device_name), None)

    if device_entry:
        average_rssi = device_entry["Average_RSSI"]
        print(f"Average RSSI of {device_name}: {average_rssi} dBm")

        # Calculate the estimated distance
        distance = calculate_distance(average_rssi)
        print(f"Estimated distance to {device_name}: {distance:.2f} meters")
        return distance
    else:
        print(f"Device '{device_name}' not found in the data.")
        return None

