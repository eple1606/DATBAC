from scapy.all import *

import os
import ctypes
import sys
import scapy

# Check if the script is running with administrative privileges on Windows
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Ensure you have the necessary permissions
if not is_admin():
    print("You need to run this script as Administrator!")
    exit(1)

# Define the callback function to process each packet
def handle_probe_request(packet):
    if packet.haslayer(Dot11ProbeReq):
        # Extract the MAC address of the device sending the probe request
        mac_address = packet.addr2
        ssid = packet.info.decode() if packet.info else "Hidden SSID"
        print(f"Probe Request captured - MAC: {mac_address}, SSID: {ssid}")

# Start sniffing for probe requests
def start_sniffing(interface):
    print(f"Starting to sniff on interface {interface}...")
    sniff(iface=interface, prn=handle_probe_request, store=0)

if __name__ == "__main__":
    # Replace 'Wi-Fi' with your wireless interface name
    wireless_interface = "Wi-Fi"
    start_sniffing(wireless_interface)