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

    # Extract and count specific features
    device_features = features.split(", ") if features else []  # Split only if features exist
    ht_count = sum(1 for f in device_features if f.startswith("HT:"))
    ext_count = sum(1 for f in device_features if f.startswith("Ext:"))
    vendor_count = sum(1 for f in device_features if f.startswith("Vendor:"))

    # Check if all feature types are missing
    all_features_missing = (ht_count == 0 and ext_count == 0 and vendor_count == 0)

    # Compare against existing device signatures
    for existing_signature, existing_device_name in device_signatures.items():
        existing_ssid, existing_mac, existing_features = existing_signature

        # Extract and count features for the existing device
        existing_feature_list = existing_features.split(", ") if existing_features else []
        existing_ht_count = sum(1 for f in existing_feature_list if f.startswith("HT:"))
        existing_ext_count = sum(1 for f in existing_feature_list if f.startswith("Ext:"))
        existing_vendor_count = sum(1 for f in existing_feature_list if f.startswith("Vendor:"))

        # Initialize match_count
        match_count = 0

        # Check SSID, MAC, and Features (HT, EXT, Vendor) for matching
        if ssid and ssid == existing_ssid:
            match_count += 1
        if mac and mac == existing_mac:
            match_count += 1
        if ht_count > 0 and ht_count == existing_ht_count:
            match_count += 1
        if ext_count > 0 and ext_count == existing_ext_count:
            match_count += 1
        if vendor_count > 0 and vendor_count == existing_vendor_count:
            match_count += 1
        
        # If all HT, EXT, and Vendor features are missing, count as 1 match
        if all_features_missing:
            match_count += 1

        # If at least 3 attributes match, assign the existing device name
        if match_count >= 3:
            return existing_device_name

    # No match found, assign a new device name
    device_name = f"Device {device_counter}"
    device_signatures[device_signature] = device_name
    device_counter += 1

    return device_name
