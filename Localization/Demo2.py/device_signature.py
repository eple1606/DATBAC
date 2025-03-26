device_signatures = {}
device_counter = 1
temporary_signatures = {}  # Store devices with very limited feature sets

def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    A device is considered the same if enough features match.
    If a device only has one feature, it is temporarily stored until more data is received.
    """

    print("------------------")
    print("New Data")
    print("------------------")
    global device_counter

    # Extract SSID, MAC, and Features
    ssid, mac, features = device_signature

    # Determine if SSID is hidden
    is_hidden_ssid = ssid == "<Hidden SSID>"

    # Extract and count features
    device_features = features.split(", ") if features else []

    # Count feature types
    ht_count = sum(1 for f in device_features if f.startswith("HT:"))
    ext_count = sum(1 for f in device_features if f.startswith("Ext:"))
    vendor_oui_count = sum(1 for f in device_features if f.startswith("Vendor OUI:"))
    vendor_info_count = sum(1 for f in device_features if f.startswith("Vendor Info:"))
    supported_rates_count = sum(1 for f in device_features if f.startswith("Supported Rates:"))
    rsn_count = sum(1 for f in device_features if f.startswith("RSN:"))

    total_features = ht_count + ext_count + vendor_oui_count + vendor_info_count + supported_rates_count + rsn_count

    print(f"New Device Signature: {device_signature}")
    print(f"Total Features Found: {total_features}")

    # Handle very limited feature sets
    if total_features <= 1:
        print("Warning: Only 1 feature detected. Storing temporarily for future validation.")

        # Check if the MAC has been seen before
        if mac in temporary_signatures:
            print("Matching previously stored temporary device.")
            return temporary_signatures[mac]

        # Store temporarily until more probe requests arrive
        device_name = f"Device {device_counter} (Unverified)"
        temporary_signatures[mac] = device_name
        return device_name

    # Full matching logic (as before)
    required_matches = 6 if not is_hidden_ssid else 5

    # Compare against existing devices
    for existing_signature, existing_device_name in device_signatures.items():
        existing_ssid, existing_mac, existing_features = existing_signature

        # If MAC address matches, return immediately
        if mac == existing_mac:
            print(f"MAC Match Found: {mac} == {existing_mac}, considering as same device.")
            return existing_device_name

        # Extract existing feature counts
        existing_feature_list = existing_features.split(", ") if existing_features else []
        existing_total_features = len(existing_feature_list)

        # Check exact feature match
        if device_features == existing_feature_list:
            print(f"Perfect feature match found with {existing_device_name}")
            return existing_device_name

    # If no match, assign a new device name
    device_name = f"Device {device_counter}"
    device_signatures[device_signature] = device_name
    device_counter += 1

    print(f"New Device Assigned: {device_name}")
    return device_name
