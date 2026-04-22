class DummySerial:
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        print(f"--- Virtual Port {port} Initialized ---")

    def write(self, data):
        # Convert the bytes to Hex so you can verify Pelco-D packets
        hex_data = data.hex().upper()
        # Split it into pairs for readability (FF 01 00...)
        formatted_hex = " ".join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
        print(f"[SERIAL OUT]: {formatted_hex}")

    def close(self):
        print("--- Virtual Port Closed ---")

    def __enter__(self): return self
    def __exit__(self, *args): self.close()

# --- Testing ---
# Instead of: ser = serial.Serial('COM3', 9600)
# Use:
ser = DummySerial('COM_MOCK', 9600)
# Your existing move_left(ser) functions will work perfectly with this!