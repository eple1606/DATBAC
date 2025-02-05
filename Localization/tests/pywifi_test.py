import time
from pywifi import PyWiFi

def continuous_scan(interval=2):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    while True:
        iface.scan()
        time.sleep(interval)
        results = iface.scan_results()

        for network in results:
            ssid = network.ssid if network.ssid else "(Hidden)"
            print(f"MAC: {network.bssid}, Signal Strength (RSSI): {network.signal}, SSID: {ssid}")
        print("-" * 40)

if __name__ == "__main__":
    continuous_scan()
