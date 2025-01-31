from scapy.all import sniff

def start_sniffing(WiFi, packet_callback, filter=None):
    """
    Starts WiFi packet sniffing on the specified interface.
    
    Args:
        interface (str): The name of the interface to sniff on.
        packet_callback (function): A callback function to handle packets.
        filter (str, optional): A BPF filter to apply to the sniffing.
    """
    print(f"Sniffing on interface: {WiFi}")
    
    # If a filter is provided, apply it to the sniffing
    sniff(iface=WiFi, prn=packet_callback, store=False, filter=filter)
