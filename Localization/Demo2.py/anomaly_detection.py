from scapy.all import Dot11ProbeReq, Dot11Elt  # Make sure Scapy is imported
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

def detect_anomalies(X, df):
    # Apply Isolation Forest for anomaly detection (to detect new devices)
    iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    df["Anomaly_Score"] = iso_forest.fit_predict(X)

    # Label "New" vs "Persistent" MACs based on anomaly scores
    df["Device_Type"] = df["Anomaly_Score"].apply(lambda x: "New Device" if x == -1 else "Persistent Device")

    # Print the results
    print(df[["MAC", "SSID", "RSSI", "Avg_Probe_Interval", "Device_Type"]])

    # Plot the results of anomaly detection (Red for "New Device" and Blue for "Persistent Device")
    #plt.figure(figsize=(10, 6))
    #colors = {"New Device": "red", "Persistent Device": "blue"}
    #plt.scatter(df.index, df["RSSI"], c=df["Device_Type"].map(colors), alpha=0.7)
    #plt.xlabel("Device Index")
    #plt.ylabel("RSSI (Signal Strength)")
    #plt.title("Anomaly Detection: New vs. Persistent Devices")
    #plt.show()
