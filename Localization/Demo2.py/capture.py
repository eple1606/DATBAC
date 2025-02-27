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

        # Filter only for "HUAWEI-5G-9Ysz" or hidden SSID
        if ssid != "HUAWEI-5G-9Ysz" and mac !="ce:0a:dd:5c:9e:f7":
            return  # Ignore packets that don't match the filter

        # DEBUG INFO
        #print(packet.summary())  # Basic packet info
        #print("split")
        #print(packet.show())     # Full packet structure
        
        
        # Extract Wi-Fi Capabilities (Rates, HT, Extended)
        wifi_features = []
        if packet.haslayer(Dot11Elt):
            try:
                elt = packet.getlayer(Dot11Elt)
                while elt:
                    print(elt.info)
                    #if elt.ID == 1:  # Supported Rates
                        #wifi_features.append(f"Rates:{elt.info.hex()}")
                    if elt.ID == 45:  # HT Capabilities
                        wifi_features.append(f"HT:{elt.info.hex()}")
                    elif elt.ID == 127:  # Extended Capabilities
                        wifi_features.append(f"Ext:{elt.info.hex()}")
                    elif elt.ID == 221:  # Vendor Specific
                        print(elt.info.hex())
                        #wifi_features.append(f"Vendor:{elt.info.hex()}")
                    # Move to the next Dot11Elt layer
                    elt = elt.payload.getlayer(Dot11Elt)

            except Exception as e:
                print(f"[!] Error parsing Dot11Elt: {e}")
                wifi_features.append("Null")

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

def start_sniffing(interface="wlan0"):
    print("[*] Listening for Wi-Fi probe requests...")
    sniff(iface=interface, prn=handle_probe_request, store=0, filter="type mgt subtype probe-req")
