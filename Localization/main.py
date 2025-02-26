import asyncio
import json
import uuid
from datetime import datetime
#from bleak import BleakScanner # Uncomment this line if using BLE scanning
from scapy.all import sniff, Dot11

# Path to the file where the devices' data will be stored
KNOWN_DEVICES_FILE = 'known_devices.json'

# Load known devices from the file if it exists
def load_known_devices():
    try:
        with open(KNOWN_DEVICES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save the known devices back to the file
def save_known_devices(known_devices):
    with open(KNOWN_DEVICES_FILE, 'w') as file:
        json.dump(known_devices, file, indent=4)

# Generate a new unique ID for a device
def generate_device_id():
    return str(uuid.uuid4())

# Get the current timestamp
def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Bluetooth Device Data Storage (Global)
known_devices = load_known_devices()  # Load the known devices from the file

# RSSI to distance conversion function (simplified model)
def rssi_to_distance(rssi):
    if rssi == 0:  # Avoid division by zero errors
        return float('inf')  # Return max distance if RSSI is zero
    return 10 ** ((27.55 - (20 * 2.4) + abs(rssi)) / 20)

# Helper function to check if RSSI is within an acceptable threshold
def is_rssi_similar(rssi1, rssi2, threshold=5):
    return abs(rssi1 - rssi2) <= threshold  # RSSI difference within threshold is considered similar

# Function to add or update a device
def add_or_update_device(device_id, wifimac, ssid, wifirssi, bluetoothmac, bluetoothname, bluetoothrssi, bluetoothadvertisement_data=None):
    global known_devices
    existing_device_id = None

    # Check if device already exists based on Bluetooth MAC address or advertisement data
    for dev_id, device in known_devices.items():
        # Check if the RSSI is similar and if the advertisement data is matching
        if (bluetoothmac in device['previous_mac_addresses'] or
            is_rssi_similar(bluetoothrssi, device['bluetoothrssi'])):
            # Further check for matching advertisement data, e.g., UUID or manufacturer data
            if bluetoothadvertisement_data:
                if 'service_uuids' in bluetoothadvertisement_data and bluetoothadvertisement_data['service_uuids'] == device.get('advertisement_data', {}).get('service_uuids'):
                    existing_device_id = dev_id
                    break
                if 'manufacturer_data' in bluetoothadvertisement_data and bluetoothadvertisement_data['manufacturer_data'] == device.get('advertisement_data', {}).get('manufacturer_data'):
                    existing_device_id = dev_id
                    break
                # Additional check for TX power (if available)
                if 'tx_power' in bluetoothadvertisement_data and bluetoothadvertisement_data['tx_power'] == device.get('advertisement_data', {}).get('tx_power'):
                    existing_device_id = dev_id
                    break
            else:
                existing_device_id = dev_id
                break

    # If device is not already present, generate a new ID and add it
    if not existing_device_id:
        device_id = generate_device_id()
        known_devices[device_id] = {
            "id": device_id,
            "wifimac": wifimac,
            "SSID": ssid,
            "wifirssi": wifirssi,
            "bluetoothmac": bluetoothmac,
            "name": bluetoothname,
            "bluetoothrssi": bluetoothrssi,
            "current_distance": rssi_to_distance(wifirssi),
            "timestamp": get_current_timestamp(),  # Add timestamp
            "previous_bluetoothmac_addresses": [bluetoothmac],  # Store the first MAC address
            "advertisement_data": bluetoothadvertisement_data or {}  # Save additional advertisement data
        }
    else:
        # Update the device data if already exists
        device = known_devices[existing_device_id]
        device["bluetoothrssi"] = bluetoothrssi
        device["current_distance"] = rssi_to_distance(bluetoothrssi)
        device["timestamp"] = get_current_timestamp()  # Update timestamp

        # If the new MAC address is different, add it to the list of previous addresses
        if bluetoothmac not in device["previous_mac_addresses"]:
            device["previous_mac_addresses"].append(bluetoothmac)  # Add to history

# Bluetooth Device Scanning (this will track movement but keep the device fixed)
async def scan_bluetooth():
    global known_devices
    print("Scanning for Bluetooth devices...")

    devices = await BleakScanner.discover()

    for device in devices:
        rssi = device.rssi  # Use the correct attribute for RSSI
        mac = device.address  # The device MAC address
        advertisement_data = device.metadata.get("advertisement_data", None)  # Get advertisement data from metadata

        device_name = f"Device {mac.replace(':', '')[:8]}"  # Assign a unique name based on the MAC address

        # Extract advertisement data if available
        advertisement_info = {}
        if advertisement_data:
            # Extract relevant information (e.g., service UUIDs, manufacturer data, TX power)
            if 'service_uuids' in advertisement_data:
                advertisement_info['service_uuids'] = advertisement_data['service_uuids']
            if 'manufacturer_data' in advertisement_data:
                advertisement_info['manufacturer_data'] = advertisement_data['manufacturer_data']
            if 'tx_power' in advertisement_data:
                advertisement_info['tx_power'] = advertisement_data['tx_power']
        
        # If the device is already known (based on RSSI or previous MAC addresses)
        add_or_update_device(None, None, None, None, mac, device_name, rssi, advertisement_info)  # Handle new or updated device
    # Save the updated devices to the file
    save_known_devices(known_devices)

# Wifi Device Scanning (this will track movement but keep the device fixed)
async def scan_wifi():
    print("Scanning for Wi-Fi devices...")

    # Define the callback function to process each packet
    def handle_probe_request(packet):
        if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 4:  # Check if it's a Probe Request
                rssi = getattr(packet, "dBm_AntSignal", None)  # Extract RSSI
                mac = packet.addr2  # Extract MAC address
                ssid = packet.info.decode() if packet.info else "Hidden SSID"  # Extract SSID

                # Add or update the device based on the MAC address
                add_or_update_device(None, mac, ssid, rssi, None, None, None, None)  # Handle new or updated device

    # Start sniffing for probe requests
    sniff(iface="wlan0", prn=handle_probe_request, store=0)  # Sniff on "wlan0" wireless interface

    save_known_devices(known_devices)  # Save the updated devices to the file



# Function to display tracked devices based on proximity
def display_devices():
    # Sort devices by distance (closest first)
    sorted_devices = sorted(known_devices.values(), key=lambda x: x['current_distance'])

    print("\nBluetooth Devices sorted by Proximity:")
    for device in sorted_devices:
        print(f"{device['name']} (MAC: {device['bluetoothmac']}) | RSSI: {device['bluetoothrssi']} | Distance: {device['current_distance']:.2f} meters | Last Seen: {device['timestamp']}")
        
        # Print advertisement data (if available)
        if device["advertisement_data"]:
            print(f"  Advertisement Data: {device['advertisement_data']}")
    print("\nWi-Fi Devices sorted by Proximity:")
    for device in sorted_devices:
        print(f"{device['name']} (MAC: {device['wifimac']}) | RSSI: {device['wifirssi']} | Distance: {device['current_distance']:.2f} meters | Last Seen: {device['timestamp']}")
        

# Continuous Scanning and Updating
async def continuous_scan():
    while True:
        #await scan_bluetooth()
        await scan_wifi()
        display_devices()
        await asyncio.sleep(5)  # Wait for 5 seconds before the next scan

# Main function to run the scanning process
if __name__ == "__main__":
    # Run the continuous scanning loop
    asyncio.run(continuous_scan())

