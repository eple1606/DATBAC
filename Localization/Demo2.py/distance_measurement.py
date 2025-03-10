import math

# Function to calculate distance from RSSI
def calculate_distance(rssi, A=-50, n=2):
    """
    Estimate the distance to a device using RSSI.
    
    :param rssi: Received Signal Strength Indicator (RSSI) in dBm.
    :param A: RSSI at 1 meter distance (default is -50 dBm).
    :param n: Path loss exponent (default is 2 for free-space, but can vary).
    :return: Estimated distance in meters.
    """
    # Calculate the distance using the RSSI formula
    distance = 10 ** ((A - rssi) / (10 * n))
    return distance

# Function to measure the distance to a known/persistent device using RSSI
def measure_distance_to_persistent_device(df_filtered, known_mac):
    """
    Measure the distance to a known/persistent device using its RSSI.
    
    :param df_filtered: DataFrame containing persistent device data.
    :param known_mac: The MAC address of the known device.
    :return: Estimated distance to the known device.
    """
    # Find the entry for the known device
    device_data = df_filtered[df_filtered["MAC"] == known_mac]

    if not device_data.empty:
        # Get the latest RSSI of the known device (you can choose the most recent, or average)
        rssi = device_data["RSSI"].iloc[-1]
        print(f"RSSI of device {known_mac}: {rssi} dBm")
        
        # Calculate the estimated distance
        distance = calculate_distance(rssi)
        print(f"Estimated distance to device {known_mac}: {distance:.2f} meters")
        return distance
    else:
        print(f"Device with MAC address {known_mac} not found in the data.")
        return None
