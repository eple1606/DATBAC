from scapy.all import Dot11, Dot11ProbeReq, Dot11Elt
from scapy.all import sniff
import time

# Global list to store captured probe data
probe_data = []

def handle_probe_request(packet):
    if packet.haslayer(Dot11ProbeReq):
        mac = packet.addr2  # Source MAC (even if randomized)
        ssid = packet.info.decode(errors="ignore") if packet.info else "<Hidden SSID>"
        rssi = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else None
        timestamp = time.time()

        # Extract Wi-Fi Capabilities (Rates, HT, Extended)
        wifi_features = []
        if packet.haslayer(Dot11Elt):
            for elt in packet.iterlayer(Dot11Elt):
                if elt.ID == 1:   # Supported Rates
                    wifi_features.append(f"Rates:{elt.info.hex()}")
                elif elt.ID == 45: # HT Capabilities
                    wifi_features.append(f"HT:{elt.info.hex()}")
                elif elt.ID == 127: # Extended Capabilities
                    wifi_features.append(f"Ext:{elt.info.hex()}")

        # Store the fingerprint
        probe_data.append({
            "MAC": mac,
            "SSID": ssid,
            "RSSI": rssi,
            "Timestamp": timestamp,
            "Features": ", ".join(wifi_features)
        })

        # Print captured details
        print(f"\n[+] Probe Request from {mac}")
        print(f"    - SSID: {ssid}")
        print(f"    - RSSI: {rssi} dBm")
        print(f"    - Features: {wifi_features}")

def start_sniffing(interface="wlan0mon"):
    print("[*] Listening for Wi-Fi probe requests...")
    sniff(iface=interface, prn=handle_probe_request, store=0, filter="type mgt subtype probe-req")
