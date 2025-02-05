from bleak import BleakScanner
import asyncio

async def scan_ble_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    if devices:
        print(f"Found {len(devices)} device(s):")
        for device in devices:
            print(f"  - Name: {device.name or 'Unknown'}, Address: {device.address}")
    else:
        print("No devices found.")

if __name__ == "__main__":
    asyncio.run(scan_ble_devices())
