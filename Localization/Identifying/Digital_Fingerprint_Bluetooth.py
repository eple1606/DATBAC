import asyncio
from bleak import BleakScanner
from collections import defaultdict
import time

# Store device fingerprints
device_fingerprints = defaultdict(lambda: {"count": 0, "manufacturer": None, "rssi_values": [], "last_seen": None})

async def scan_bluetooth():
    print(" Scanning for Bluetooth devices...")
    
    def callback(device, advertisement_data):
        mac = device.address
        rssi = device.rssi
        manufacturer_data = advertisement_data.manufacturer_data

        # Fingerprinting logic
        device_fingerprints[mac]["count"] += 1  # Increment seen count
        device_fingerprints[mac]["rssi_values"].append(rssi)  # Track RSSI values
        device_fingerprints[mac]["last_seen"] = time.time()  # Timestamp of last detection
        
        if manufacturer_data:
            device_fingerprints[mac]["manufacturer"] = manufacturer_data

        # Print detected device
        print(f"Device: {mac} | RSSI: {rssi} | Manufacturer: {manufacturer_data}")

    # Start BLE scanning
    scanner = BleakScanner(callback)
    await scanner.start()
    await asyncio.sleep(10)  # Scan for 10 seconds
    await scanner.stop()

    print("Device Fingerprints:")
    for mac, data in device_fingerprints.items():
        avg_rssi = sum(data['rssi_values']) / len(data['rssi_values']) if data['rssi_values'] else 0
        print(f" MAC: {mac} | Seen: {data['count']} times | Avg RSSI: {avg_rssi:.2f} | Manufacturer: {data['manufacturer']}")

# Run the Bluetooth scanner
asyncio.run(scan_bluetooth())
