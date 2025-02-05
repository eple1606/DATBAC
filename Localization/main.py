import sys
import os
import Identifying
import sniffing.Formula
import sniffing

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sniffing.packet_sniffer import start_sniffing
from Localization.Identifying.device_identifier import DeviceIdentifier

if __name__ == "__main__":
    # Load the OUI data for device identification
    identifier = DeviceIdentifier(oui_file=os.path.join(os.path.dirname(__file__), "data", "oui.csv"))

    def packet_callback(packet):
        """
        Callback function for processing sniffed packets.
        """
        print("Packet captured: ", packet.summary())  # Debugging line to show the packet

        # Check if the packet has the Dot11ProbeReq layer (Probe Request)
        if packet.haslayer("Dot11ProbeReq"):
            mac_address = packet.addr2
            device_vendor = identifier.identify_device(mac_address)
            print(f"Detected Probe Request from {mac_address} ({device_vendor})")
        else:
            print(f"Captured a non-Probe Request packet: {packet.summary()}")

    # Start WiFi sniffing on the specified interface
    interface = "WiFi"  # Use the correct interface name (WiFi on Windows)
    print(f"Starting sniffing on {interface}...")

    # Start sniffing without any filters (to capture all packets)
    start_sniffing(interface, packet_callback)
