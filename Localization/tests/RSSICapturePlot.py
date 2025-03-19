from scapy.all import *
import time
import statistics
import matplotlib.pyplot as plt

# Change this to the MAC prefix you're interested in (first 3 bytes of MAC address)
TARGET_MAC_PREFIX = "de:0f:c5:13:d9:ec"
OUTPUT_FILE = "RSSI_Log.txt"

# Function to capture RSSI values from probe requests
def capture_rssi(interface, duration, target_prefix):
    rssi_values = []
    timestamps = []
    start_time = time.time()
    
    def handle_probe_request(packet):
        if packet.haslayer(Dot11ProbeReq) and packet.haslayer(RadioTap):
            mac = packet.addr2
            ssid = packet.info.decode(errors="ignore") if packet.info else "<Hidden SSID>"

            # Filter only for "HUAWEI-5G-9Ysz" or MAC
            if ssid != "HUAWEI-5G-9Ysz" and mac != target_prefix:
                return  # Ignore packets that don't match the filter

            rssi = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else None
            if rssi is not None:
                timestamp = time.time() - start_time
                rssi_values.append(rssi)
                timestamps.append(timestamp)
                print(f"[{timestamp:.2f}s] Captured RSSI: {rssi} dBm from {mac}")
    
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    sniff(iface=interface, prn=handle_probe_request, timeout=duration/10)
    return timestamps, rssi_values

# Function to save RSSI measurements to a file
def save_results(timestamps, rssi_values):
    avg_rssi = statistics.mean(rssi_values) if rssi_values else "No data captured"
    
    with open(OUTPUT_FILE, "w") as f:
        f.write("Time (s), RSSI (dBm)\n")
        for t, rssi in zip(timestamps, rssi_values):
            f.write(f"{t:.2f}, {rssi}\n")
        f.write(f"\nAverage RSSI: {avg_rssi}\n")
    
    print(f"Data saved to {OUTPUT_FILE}")

# Function to plot RSSI over time
def plot_rssi(timestamps, rssi_values):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, rssi_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Time (seconds)")
    plt.ylabel("RSSI (dBm)")
    plt.title("RSSI Over Time")
    plt.grid()
    plt.show()

# Main function
def main():
    interface = "wlan0"  # Change this to your monitoring interface
    duration = 300  # Run for 5 minutes
    
    print("Starting RSSI capture for 5 minutes...")
    timestamps, rssi_values = capture_rssi(interface, duration, TARGET_MAC_PREFIX)
    save_results(timestamps, rssi_values)
    
    if rssi_values:
        plot_rssi(timestamps, rssi_values)
    print("Script finished.")
    
if __name__ == "__main__":
    main()