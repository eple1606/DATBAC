from scapy.all import sniff, Dot11
import math
import matplotlib.pyplot as plt
import numpy as np

# Predefined MAC addresses to filter
FILTER_MACS = {
    "ce:0a:dd:5c:9e:f7": "Device 1",
    "AA:BB:CC:DD:EE:FF": "Device 2"
}

# Ask user whether to filter MAC addresses or not
filter_choice = input("Do you want to filter by the predefined MAC addresses? (y/n): ").strip().lower()

# Constants for distance calculation
TX_POWER_DBM = -30  # Approximate Tx power of a mobile device (in dBm)
PATH_LOSS_EXPONENT = 3  # Free-space propagation

# Initialize plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_title("Wi-Fi Probe Request Sonar")
ax.set_ylim(0, 500)
ax.set_xticks(np.linspace(0, 2*np.pi, 8))
ax.set_yticks(range(0, 500, 100))

devices = {}

def rssi_to_distance(rssi):
    """Convert RSSI (dBm) to distance in cm."""
    try:
        distance_m = 10 ** ((TX_POWER_DBM - rssi) / (10 * PATH_LOSS_EXPONENT))
        return distance_m * 100  # Convert meters to cm
    except:
        return None

def update_plot():
    """Update sonar plot with detected devices."""
    ax.clear()
    ax.set_title("Wi-Fi Probe Request Sonar")
    ax.set_ylim(0, 500)
    ax.set_xticks(np.linspace(0, 2*np.pi, 8))
    ax.set_yticks(range(0, 500, 100))

    angles, distances, labels = [], [], []
    for i, (mac, data) in enumerate(devices.items()):
        angles.append(i * (2 * np.pi / len(devices)))  # Spread devices in a circle
        distances.append(data["distance"])
        labels.append(f"{data['name']} ({data['distance']:.1f}cm)")

    ax.scatter(angles, distances, c='r', s=50, label="Devices")
    for i, label in enumerate(labels):
        ax.text(angles[i], distances[i], label, fontsize=8, ha='center', color='white')

    plt.pause(0.5)  # Refresh rate

def handle_probe_request(packet):
    """Capture and process probe requests."""
    if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 4:  # Probe Request
        mac = packet.addr2
        ssid = packet.info.decode('utf-8', errors='ignore') if packet.info else "<Hidden>"
        rssi = getattr(packet, "dBm_AntSignal", None)
        distance_cm = rssi_to_distance(rssi) if rssi is not None else None

        # Apply filtering if user chose 'y'
        if filter_choice == 'y' and mac not in FILTER_MACS:
            return

        device_name = FILTER_MACS.get(mac, f"Unknown ({mac})") if filter_choice == 'y' else f"Device {len(devices) + 1}"
        devices[mac] = {"name": device_name, "ssid": ssid, "rssi": rssi, "distance": distance_cm}

        print(f"[+] {device_name} | MAC: {mac} | SSID: {ssid} | RSSI: {rssi} dBm | Distance: {distance_cm:.1f} cm")
        update_plot()

# Start sniffing
tracking_text = f"Tracking specific MACs: {list(FILTER_MACS.keys())}" if filter_choice == 'y' else "Tracking ALL probe requests"
print(f"{tracking_text}... (Press Ctrl+C to stop)")

sniff(iface="wlan0", prn=handle_probe_request, store=0)