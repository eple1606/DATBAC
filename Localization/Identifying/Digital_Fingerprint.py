from scapy.all import sniff, Dot11ProbeReq, Dot11Elt
import time
import hashlib
import json

# Dictionary to store observed device fingerprints
device_fingerprints = {}

def hash_fingerprint(data):
    """Creates a unique hash from extracted fingerprint data."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def extract_fingerprint(packet):
    """Extracts fingerprinting features from a probe request packet."""
    
    fingerprint = {}
    
    # Get MAC Address (randomized)
    fingerprint["mac_address"] = packet.addr2
    
    # Get sequence number (used to detect device movement & request patterns)
    fingerprint["sequence_number"] = packet.SC

    # Capture probe request intervals (inter-arrival time)
    current_time = time.time()
    if packet.addr2 in device_fingerprints:
        last_time = device_fingerprints[packet.addr2]["last_seen"]
        fingerprint["inter_arrival_time"] = round(current_time - last_time, 4)
    else:
        fingerprint["inter_arrival_time"] = None  # First request seen
    
    fingerprint["last_seen"] = current_time  # Update last seen time
    
    # Extract SSIDs the device is probing for
    ssids = []
    for elt in packet.iter_payloads():
        if isinstance(elt, Dot11Elt) and elt.ID == 0:  # SSID element
            ssids.append(elt.info.decode(errors="ignore"))
    
    fingerprint["probe_ssids"] = ssids
    
    # Extract vendor-specific information
    fingerprint["vendor_elements"] = []
    for elt in packet.iter_payloads():
        if isinstance(elt, Dot11Elt) and elt.ID == 221:  # Vendor-specific information
            fingerprint["vendor_elements"].append(elt.info.hex())

    # Create a unique hash for this fingerprint
    fingerprint["fingerprint_hash"] = hash_fingerprint(fingerprint)
    
    return fingerprint

def packet_callback(packet):
    """Processes captured packets and logs fingerprint information."""
    if packet.haslayer(Dot11ProbeReq):
        fingerprint = extract_fingerprint(packet)
        mac_address = fingerprint["mac_address"]
        
        # Save fingerprint
        device_fingerprints[mac_address] = fingerprint
        
        # Print device fingerprint
        print(f"Captured Probe Request from {mac_address}")
        print(json.dumps(fingerprint, indent=4))

# Start sniffing for Probe Request packets
def start_sniffing(interface="wlan0"):
    print(f"Starting Wi-Fi probe request sniffing on {interface}...")
    sniff(iface=interface, prn=packet_callback, store=False, monitor=True)

# Run the sniffer (Replace 'wlan0' with your Wi-Fi interface)
if __name__ == "__main__":
    start_sniffing("wlan0")
