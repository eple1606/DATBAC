import asyncio

# Device signature dictionary to store device names associated with MAC address, SSID, and features
device_signatures = {}
device_counter = 1
device_signatures_lock = asyncio.Lock()  # Lock for thread safety when modifying the dictionary

def extract_features(features):
    """Extracts feature counts from the feature string."""
    feature_dict = {"HT": 0, "Ext": 0, "Vendor": 0}
    if features:
        for feature in features.split(", "):
            for key in feature_dict:
                if feature.startswith(key + ":"):
                    feature_dict[key] += 1
    return feature_dict

async def get_device_name(device_signature):
    """
    Assigns or retrieves the device name based on the device signature.
    - Immediate match on MAC address.
    - If SSID is hidden, uses a lower matching threshold.
    """
    global device_counter
    
    ssid, mac, features = device_signature
    feature_counts = extract_features(features)
    is_hidden_ssid = not ssid or ssid.lower() == "hidden"
    
    # Adjust match threshold based on SSID visibility
    required_matches = 2 if is_hidden_ssid else 3  # Match 2 features if SSID is hidden, 3 if visible

    # Log device signature for debugging
    print(f"Processing Device Signature: SSID={ssid}, MAC={mac}, Features={features}")

    async with device_signatures_lock:
        # Keep track of all matching MAC addresses
        matched_macs = []

        # Look for a matching device in the existing signatures
        for existing_signature, existing_device_name in device_signatures.items():
            existing_ssid, existing_mac, existing_features = existing_signature

            # Immediate match on MAC address
            if mac == existing_mac:
                print(f"MAC Match Found: {mac}, same device.")
                return existing_device_name

            # Compare feature counts only for features that exist in both the current and existing signatures
            existing_feature_counts = extract_features(existing_features)
            match_count = 0

            # Check matching features (HT, Ext, Vendor)
            for key in feature_counts:
                if key in existing_feature_counts and feature_counts[key] > 0 and feature_counts[key] == existing_feature_counts[key]:
                    match_count += 1

            # If SSID is visible, we also match on SSID
            if not is_hidden_ssid and ssid == existing_ssid:
                match_count += 1

            # If feature match count exceeds the threshold, this is a match
            if match_count >= required_matches:
                print(f"Matched with existing device: {existing_device_name} (MAC: {mac}, SSID: {ssid})")
                
                # Add the existing MAC to the list of matched MACs
                matched_macs.append(existing_mac)

        # If no match was found, assign a new device name
        if not matched_macs:
            device_name = f"Device {device_counter}"
            device_signatures[(ssid, mac, features)] = device_name
            device_counter += 1
            print(f"New Device Assigned: {device_name} (MAC: {mac}, SSID: {ssid})")
        else:
            # If we found matches, print all the corresponding MACs
            print(f"[+] Device labeled as an old device (MAC: {mac})")
            print(f"    - Corresponding MAC addresses: {', '.join(matched_macs)}")

            # Return the first device name that matched (assuming multiple MACs correspond to the same device)
            device_name = device_signatures.get((ssid, matched_macs[0], features))

        return device_name
