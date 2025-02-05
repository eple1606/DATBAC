import asyncio
from bleak import BleakScanner

# Constants for RSSI to Distance Conversion
A = -70  # RSSI value at 1 meter (calibration constant, adjust as needed)
n = 2.0  # Path-loss exponent (adjust for your environment)

def calculate_distance(rssi):
    """
    Convert RSSI to distance in centimeters using the Bluetooth formula.
    """
    if rssi == 0:
        return float('inf')  # Return infinity if RSSI is zero (no signal)
    
    # Convert RSSI to distance in meters
    distance_meters = 10 ** ((A - rssi) / (10 * n))
    # Convert meters to centimeters
    distance_cm = distance_meters * 100
    return distance_cm

async def track_devices():
    print("Starting live RSSI tracking...")
    while True:
        devices = await BleakScanner.discover()
        if devices:
            print("\033c", end="")  # Clear terminal for a live update effect
            print(f"Found {len(devices)} device(s):")
            for device in devices:
                name = device.name or "Unknown"
                rssi = device.rssi
                distance = calculate_distance(rssi)
                print(f"  - Name: {name}, Address: {device.address}, RSSI: {rssi} dBm, Distance: {distance:.2f} cm")
        else:
            print("No devices found.")
        await asyncio.sleep(1)  # Scan every 1 seconds

if __name__ == "__main__":
    asyncio.run(track_devices())
