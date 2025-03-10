import numpy as np

def calculate_distance_from_rssi(average_rssi, A=-40, n=2):
    """
    Calculates the distance based on the average RSSI using the Log Distance Path Loss Model.
    
    :param average_rssi: Average RSSI for a device (in dBm)
    :param A: RSSI at a reference distance (usually 1 meter, default: -40 dBm)
    :param n: Path loss exponent (default: 2)
    :return: Estimated distance in meters
    """
    distance = 10 ** ((A - average_rssi) / (10 * n))
    return distance


def calculate_device_distances(average_rssi):
    """
    Calculates the estimated distance for each device based on its average RSSI value.
    
    :param average_rssi: Dictionary containing the average RSSI for each device (Device_Name)
    :return: Dictionary of distances for each device
    """
    device_distances = {}
    
    for device_name, avg_rssi in average_rssi.items():
        distance = calculate_distance_from_rssi(avg_rssi)
        device_distances[device_name] = distance
    
    return device_distances
