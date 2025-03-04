from scapy.all import *
import time
import statistics

# Change this to the MAC prefix you're interested in (first 3 bytes of MAC address)
TARGET_MAC_PREFIX = "de:0f:c5:13:d9:ec"
OUTPUT_FILE = "RSSI_DistanceMeasurements.txt"

# Function to capture RSSI values from probe requests
def capture_rssi(interface, duration, target_prefix):
    rssi_values = []
    
    def handle_probe_request(packet):
        if packet.haslayer(Dot11ProbeReq) and packet.haslayer(RadioTap):
            mac = packet.addr2
            ssid = packet.info.decode(errors="ignore") if packet.info else "<Hidden SSID>"/

            # Filter only for "HUAWEI-5G-9Ysz" or MAC
            if ssid !="HUAWEI-5G-9Ysz" and mac !="de:0f:c5:13:d9:ec":
                return  # Ignore packets that don't match the filter


            rssi = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else None
            if rssi is not None:
                rssi_values.append(rssi)
                if duration < 20:
                    print("Less than 20 seconds until next measurement")
                print(f"Captured RSSI: {rssi} dBm from {mac_address}")
    
    sniff(iface=interface, prn=handle_probe_request, timeout=duration)
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
    duration = 120  # Capture duration for each distance in seconds
    distances = [0, 1, 2, 3]  # Distances in meters
    
    for distance in distances:
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        print(f"Starting capture for {distance} meter(s)...")
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        rssi_values = capture_rssi(interface, duration, TARGET_MAC_PREFIX)
        save_results(distance, rssi_values)
        print(f"Finished capture for {distance} meter(s). Data saved.")
        time.sleep(10)  # Short delay before next capture
    
if __name__ == "__main__":
    main()
