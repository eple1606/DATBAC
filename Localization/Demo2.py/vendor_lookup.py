import csv

# Global OUI dictionary
OUI_DB = {}

def load_oui_database(csv_file="oui.csv"):
    """
    Loads OUI data from a CSV file into a dictionary.
    """
    global OUI_DB
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header

            for row in reader:
                if len(row) < 3:
                    continue  # Skip malformed rows
                
                oui = row[1].strip().upper()  # Extract OUI (first 3 bytes of MAC)
                vendor = row[2].strip()       # Extract Vendor name
                
                # Store OUI in XX:XX:XX format
                OUI_DB[f"{oui[:2]}:{oui[2:4]}:{oui[4:6]}"] = vendor

    except Exception as e:
        print(f"[!] Error loading OUI database: {e}")

def get_vendor(mac):
    """
    Extracts the vendor from a MAC address using the OUI lookup.
    """
    if mac is None:
        return "Unknown"

    oui_prefix = mac.upper()[:8]  # First 3 bytes in XX:XX:XX format

    return OUI_DB.get(oui_prefix, "Unknown")  # Return vendor if found, else "Unknown"

# Load OUI database when the script is imported
load_oui_database("oui.csv")
