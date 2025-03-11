from scapy.all import Dot11, Dot11ProbeReq, Dot11Elt
from scapy.all import sniff
import time
import asyncio

# Global list to store captured probe data
probe_data = []

def handle_probe_request(packet):
    if packet.haslayer(Dot11ProbeReq):
        mac = packet.addr2  # Source MAC (even if randomized)
        ssid = packet.info.decode(errors="ignore") if packet.info else "<Hidden SSID>"
        
        # Filter only for "HUAWEI-5G-9Ysz" or hidden SSID
        #if ssid != "HUAWEI-5G-9Ysz" and mac !="de:0f:c5:13:d9:ec":
         #   return  # Ignore packets that don't match the filter

        rssi = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else None
        #print(f"Raw RSSI: {rssi}, Adjusted RSSI: {rssi - 256 if rssi > 0 else rssi}")
        timestamp = time.time()
        
        # DEBUG INFO
        #print(packet.summary())  # Basic packet info
        #print("split")
        #print(packet.show())     # Full packet structure
        
        
        # Extract Wi-Fi Capabilities (HT, Extended, Vendor)
        wifi_features = []
        if packet.haslayer(Dot11Elt):
            try:
                elt = packet.getlayer(Dot11Elt)
                while elt:
                    if elt.ID == 45:  # HT Capabilities
                        wifi_features.append(f"HT:{elt.info.hex()}")
                    elif elt.ID == 127:  # Extended Capabilities
                        wifi_features.append(f"Ext:{elt.info.hex()}")
                    elif elt.ID == 221:  # Vendor Specific (Extract OUI and info)
                        vendor_oui = elt.info[:3].hex().upper()  # Get OUI (first 3 bytes)
                        vendor_info = elt.info[3:].hex().upper()  # Get vendor-specific data after OUI
                        
                        # Add vendor-specific info to the wifi_features
                        wifi_features.append(f"Vendor:{vendor_oui}")
                        wifi_features.append(f"VendorInfo:{vendor_info}")
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
        #print(f"\n[+] Probe Request from {mac}")
        #print(f"    - SSID: {ssid}")
        #print(f"    - RSSI: {rssi} dBm")
        #print(f"    - Features: {wifi_features}")

async def start_sniffing(interface="wlan0"):
    while True:
        duration = 10
        print("[*] Listening for Wi-Fi probe requests...")
        sniff(iface=interface, prn=handle_probe_request, store=0, filter="type mgt subtype probe-req", timeout=duration)
        await asyncio.sleep(2)