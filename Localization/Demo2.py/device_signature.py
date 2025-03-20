device_signatures = {}
device_counter = 1

def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    A device is considered the same if 2 or more attributes (SSID, MAC, HT, EXT, or Vendor) match.
    """
    global device_counter

    # Extract SSID, MAC, and Features
    ssid, mac, features = device_signature

    # Extract and count specific features
    device_features = features.split(", ")  # Split the Features string into a list
    ht_count = sum(1 for f in device_features if f.startswith("HT:"))
    ext_count = sum(1 for f in device_features if f.startswith("Ext:"))
    vendor_count = sum(1 for f in device_features if f.startswith("Vendor:"))

    # Compare against existing device signatures
    for existing_signature, existing_device_name in device_signatures.items():
        existing_ssid, existing_mac, existing_features = existing_signature

        # Extract and count features for the existing device
        existing_feature_list = existing_features.split(", ")
        existing_ht_count = sum(1 for f in existing_feature_list if f.startswith("HT:"))
        existing_ext_count = sum(1 for f in existing_feature_list if f.startswith("Ext:"))
        existing_vendor_count = sum(1 for f in existing_feature_list if f.startswith("Vendor:"))

        # Count matching attributes separately
        match_count = sum([
            ssid == existing_ssid,        # Match SSID
            mac == existing_mac,          # Match MAC
            ht_count == existing_ht_count,    # Match HT feature count
            ext_count == existing_ext_count,  # Match EXT feature count
            vendor_count == existing_vendor_count  # Match Vendor feature count
        ])

        # If at least 2 attributes match, assign the existing device name
        if match_count >= 4:
            return existing_device_name

    # No match found, assign a new device name
    device_name = f"Device {device_counter}"
    device_signatures[device_signature] = device_name
    device_counter += 1

    return device_name
