from scapy.all import *
import time
import statistics

# Change this to the MAC prefix you're interested in (first 3 bytes of MAC address)
TARGET_MAC_PREFIX = "ce:0a:dd:5c:9e:f7"
OUTPUT_FILE = "RSSI_DistanceMeasurements.txt"

# Function to capture RSSI values from probe requests
def capture_rssi(interface, duration, target_prefix):
    rssi_values = []
    
    def packet_handler(pkt):
        if pkt.haslayer(Dot11ProbeReq) and pkt.haslayer(RadioTap):
            mac_address = pkt.addr2
            if mac_address and mac_address.startswith(target_prefix):
                rssi = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else None
                if rssi is not None:
                    rssi_values.append(rssi)
                    print(f"Captured RSSI: {rssi} dBm from {mac_address}")
    
    sniff(iface=interface, prn=packet_handler, timeout=duration)
    return rssi_values

# Function to save RSSI measurements to a file
def save_results(distance, rssi_values):
    if rssi_values:
        avg_rssi = statistics.mean(rssi_values)
    else:
        avg_rssi = "No data captured"
    
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"Distance: {distance} meters\n")
        f.write(f"RSSI values: {rssi_values}\n")
        f.write(f"Average RSSI: {avg_rssi}\n\n")
    
# Main function to run captures at different distances
def main():
    interface = "wlan0"  # Change this to your monitoring interface
    duration = 10  # Capture duration for each distance in seconds
    distances = [1, 2, 3]  # Distances in meters
    
    for distance in distances:
        print(f"Starting capture for {distance} meter(s)...")
        rssi_values = capture_rssi(interface, duration, TARGET_MAC_PREFIX)
        save_results(distance, rssi_values)
        print(f"Finished capture for {distance} meter(s). Data saved.")
        time.sleep(5)  # Short delay before next capture
    
if __name__ == "__main__":
    main()
