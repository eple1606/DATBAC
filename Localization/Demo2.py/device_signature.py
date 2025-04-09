import json

def load_config(filename="config.json"):
    with open(filename, "r") as file:
        return json.load(file)
config = load_config()

# Accessing values from the config
required_matches_config = config["device_signature"]["required_matches"]

device_signatures = {}
device_counter = 1

def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    A device is considered the same if 3 or more attributes (SSID, MAC, HT, EXT, or Vendor) match.
    If all three features (HT, EXT, and Vendor) are missing, it counts as 1 match.
    """
    global device_counter
    
    # Extract SSID, MAC, and Features
    ssid, mac, features = device_signature

    # Determine if SSID is hidden (empty or None ssid implies hidden)
    is_hidden_ssid = ssid == "<Hidden SSID>"

    # Extract and count specific features
    device_features = features.split(", ") if features else []  # Split only if features exist
    
        # If the match count meets the threshold, return the existing device name
        if match_count >= required_matches:
            print(f"Matched with {existing_device_name}")
            return existing_device_name

    # No match found, assign a new device name
    device_name = f"Device {device_counter}"
    device_signatures[device_signature] = device_name
    device_counter += 1

    print(f"New Device Assigned: {device_name}")
    return device_name