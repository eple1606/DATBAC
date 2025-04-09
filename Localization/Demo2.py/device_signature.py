import json
import time
from collections import defaultdict

# Load configuration
def load_config(filename="config.json"):
    with open(filename, "r") as file:
        return json.load(file)

config = load_config()

# Accessing values from the config
required_matches_config = config["device_signature"]["required_matches"]

device_signatures = {}  # Existing devices
device_counter = 1  # To assign new device IDs
temp_devices = defaultdict(list)  # Temporary devices in Batch 1
semi_devices = defaultdict(list)  # Devices in Batch 2
device_time_stamps = {}  # Time of last capture for each device

# SSID matching threshold (70% similarity)
SSID_MATCH_THRESHOLD = 0.7

# Helper functions
def calculate_ssid_match_percentage(ssids_a, ssids_b):
    """ Calculate the percentage of SSIDs that match between two sets of SSIDs. """
    common_ssids = set(ssids_a).intersection(set(ssids_b))
    return len(common_ssids) / len(set(ssids_a)) if ssids_a else 0

def device_age(mac):
    """ Return the time difference between the current time and the last seen time of the device. """
    return time.time() - device_time_stamps.get(mac, 0)

def get_device_name(device_signature, ssid_match_priority=True):
    global device_counter

    ssid, mac, features = device_signature
    device_time_stamps[mac] = time.time()  # Update last seen time for the device

    # Handle Temporary Devices in Batch 1
    if mac not in temp_devices:
        temp_devices[mac].append(device_signature)

    # Process Batch 2 (semi-stored devices) after a specific time window
    if mac in semi_devices:
        # Compare SSID matches first, if the match is strong enough, prioritize SSID
        for stored_device in semi_devices[mac]:
            stored_ssids = [d[0] for d in stored_device]  # Extract all SSIDs for comparison
            temp_ssids = [d[0] for d in temp_devices[mac]]

            ssid_match_percentage = calculate_ssid_match_percentage(stored_ssids, temp_ssids)
            if ssid_match_percentage >= SSID_MATCH_THRESHOLD:
                # Skip to features check if SSID match is sufficient
                return stored_device[0][1]  # Return the first device name

        # Fallback to features comparison if SSID match is too low
        for existing_signature, existing_device_name in device_signatures.items():
            existing_ssid, existing_mac, existing_features = existing_signature

            if mac == existing_mac:
                # Prioritize SSID match, then check features if needed
                existing_features = existing_features.split(", ")
                match_count = sum(1 for f in existing_features if f in features.split(", "))
                if match_count >= required_matches_config:
                    return existing_device_name

    # After SSID match check, fallback to batch comparison by checking features
    # Check against existing devices (Batch 3)
    for existing_signature, existing_device_name in device_signatures.items():
        existing_ssid, existing_mac, existing_features = existing_signature

        # Compare SSID
        if ssid == existing_ssid:
            return existing_device_name

        # Extract and count features for the existing device
        existing_feature_list = existing_features.split(", ") if existing_features else []
        existing_match_count = sum(1 for f in existing_feature_list if f in features.split(", "))

        if existing_match_count >= required_matches_config:
            return existing_device_name

    # No match found, assign a new device name
    device_name = f"Device {device_counter}"
    device_signatures[device_signature] = device_name
    device_counter += 1

    return device_name
