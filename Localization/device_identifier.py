import pandas as pd

class DeviceIdentifier:
    def __init__(self, oui_file):
        """
        Initialize the device identifier with OUI data.
        
        Args:
            oui_file (str): Path to the OUI CSV file.
        """
        # Load OUI data into memory
        self.oui_data = pd.read_csv(oui_file)
        self.oui_data['Assignment'] = self.oui_data['Assignment'].str.upper()

    def identify_device(self, mac_address):
        """
        Identifies a device based on its MAC address.
        
        Args:
            mac_address (str): The MAC address of the device (e.g., '10:E9:92:AA:BB:CC').
        
        Returns:
            str: The organization name associated with the MAC address or 'Unknown'.
        """
        # Extract the first 6 characters (ignoring case and colons)
        mac_prefix = mac_address.upper().replace(":", "")[:6]

        # Search for the MAC prefix in the OUI data
        match = self.oui_data[self.oui_data['Assignment'] == mac_prefix]

        if not match.empty:
            return match.iloc[0]['Organization Name']
        return "Unknown"
