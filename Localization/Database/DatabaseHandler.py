import sqlite3

def initialize_db():
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                        id INTEGER PRIMARY KEY,
                        mac_address TEXT,
                        device_type TEXT,
                        signal_strength INTEGER)''')
    conn.commit()
    return conn

def save_device(conn, device):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO devices (mac_address, device_type, signal_strength) VALUES (?, ?, ?)",
                   (device.mac_address, device.device_type, device.signal_strength))
    conn.commit()
