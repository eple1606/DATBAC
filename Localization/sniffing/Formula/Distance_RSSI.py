import math
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sniffing.packet_sniffer import start_sniffing
from Localization.Identifying.device_identifier import DeviceIdentifier

# Constants
REFERENCE_RSSI = -40  # RSSI value at 1 meter (example value, needs calibration)
PATH_LOSS_EXPONENT = 2.0  # Path loss exponent (adjust based on environment)

def calculate_distance(rssi):
    """
    Estimate the distance based on the RSSI value.
    
    Args:
        rssi (float): The RSSI value of the signal (in dBm).
        
    Returns:
        float: The estimated distance in meters.
    """
    distance = 10 ** ((REFERENCE_RSSI - rssi) / (10 * PATH_LOSS_EXPONENT))
    return distance

def packet_callback(packet):
    """
    Callback function for processing sniffed packets.
    """
    if packet.haslayer("Dot11ProbeReq"):
        mac_address = packet.addr2
        rssi = packet.dBm_AntSignal  # This gives the RSSI value (in dBm)
        
        # Calculate distance based on RSSI
        estimated_distance = calculate_distance(rssi)
        
        print(f"Detected Probe Request from {mac_address} (RSSI: {rssi} dBm) - Estimated Distance: {estimated_distance:.2f} meters")

if __name__ == "__main__":
    # Load the OUI data for device identification
    identifier = DeviceIdentifier(oui_file=os.path.join(os.path.dirname(__file__), "data", "oui.csv"))

    # Start WiFi sniffing on the specified interface
    interface = "WiFi"
    print(f"Starting sniffing on {interface}...")
    start_sniffing(interface, packet_callback, filter="wlan type mgt subtype probe-req")
