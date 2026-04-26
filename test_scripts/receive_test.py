"""Receive Test Script for Pelco-D Protocol"""

import serial

# Change 'COM5' to the port of your second adapter
RX_PORT = 'COM7'
baud_rate = 9600

try:
    with serial.Serial(RX_PORT, baud_rate, timeout=0.1) as ser:
        print(f"Monitoring {RX_PORT} for Pelco-D packets... (Ctrl+C to stop)")

        while True:
            # Look for the sync byte (0xFF)
            if ser.read(1) == b'\xff':
                # Read the remaining 6 bytes of the packet
                remaining = ser.read(6)
                if len(remaining) == 6:
                    full_packet = b'\xff' + remaining
                    print(f"Received Packet: {full_packet.hex().upper()}")

                    # Optional: Verify Checksum logic
                    calc_sum = sum(remaining[:-1]) % 256
                    if calc_sum == remaining[-1]:
                        print("  Status: [CHECKSUM VALID]")
                    else:
                        print(f"  Status: [CHECKSUM ERROR] Expected {hex(calc_sum)}")

except serial.SerialException as e:
    print(f"Error: Could not open {RX_PORT}.")
except KeyboardInterrupt:
    print("\nStopping monitor.")
