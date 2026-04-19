import serial
import time

# Change 'COM6' to the port of your first adapter
TX_PORT = 'COM6'
BAUD_RATE = 9600

def send_pelco_d(ser, address, cmd2, pan_speed, tilt_speed):
    """
    Standard 7-byte Pelco-D Packet:
    [Sync, Address, Command1, Command2, Data1, Data2, Checksum]
    """
    sync = 0xFF
    cmd1 = 0x00  # Usually 0 for standard movement

    # Checksum = (Sum of bytes 2 through 6) % 256
    checksum = (address + cmd1 + cmd2 + pan_speed + tilt_speed) % 256

    packet = bytearray([sync, address, cmd1, cmd2, pan_speed, tilt_speed, checksum])
    ser.write(packet)
    return packet.hex().upper()

try:
    with serial.Serial(TX_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Controller started on {TX_PORT}. Sending 'Pan Left'...")

        # Address 1, Command 0x04 (Left), Pan Speed 0x20, Tilt 0x00
        for _ in range(2):  # Send the command multiple times for testing
            hex_sent = send_pelco_d(ser, 1, 0x04, 0x20, 0x00) # Pan Left
            print(f"Sent: {hex_sent} (Pan Left)")
            time.sleep(1)  # Wait a bit before sending the next command
        hex_sent = send_pelco_d(ser, 1, 0x08, 0x00, 0x20)  # Tilt Up
        print(f"Sent: {hex_sent} (Tilt Up)")
        hex_sent = send_pelco_d(ser, 1, 0x00, 0x00, 0x00)  # Stop command
        print(f"Sent: {hex_sent} (Stop)")
        for _ in range(2):
            hex_sent = send_pelco_d(ser, 1, 0x02, 0x20, 0x00)  # Pan Right
            print(f"Sent: {hex_sent} (Pan Right)")
            time.sleep(1)
        hex_sent = send_pelco_d(ser, 1, 0x00, 0x00, 0x00)  # Stop command
        print(f"Sent: {hex_sent} (Stop)")

except serial.SerialException as e:
    print(f"Error: Could not open {TX_PORT}. Is it plugged in?")
