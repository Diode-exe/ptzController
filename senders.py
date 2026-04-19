class SenderFunctions:
    def __init__(self):
        pass

    def ptz_command(self, ser, address, cmd2, pan_speed=0, tilt_speed=0):
        """
        Base function to send Pelco-D packets.
        cmd2: The direction bitmask (0x02 for Right, 0x04 for Left, etc.)
        Byte 1: Sync (0xFF)
        Byte 2: Address
        Byte 3: Command 1 (Usually 0x00)
        Byte 4: Command 2 (Direction)
        Byte 5: Pan Speed (0x00 - 0x3F)
        Byte 6: Tilt Speed (0x00 - 0x3F)
        """

        packet = bytearray([0xFF, address, 0x00, cmd2, pan_speed, tilt_speed])

        # Calculate Checksum: (Bytes 2+3+4+5+6) % 256
        checksum = sum(packet[1:]) % 256
        packet.append(checksum)

        ser.write(packet)
        return packet.hex().upper()

# --- Directional Functions ---

    def stop(self, ser, addr=1):
        """Sends a stop command (no movement)"""
        return self.ptz_command(ser, addr, 0x00, 0, 0)

    def move_up(self, ser, addr=1, speed=0x20):
        """Sends a command to move the camera up"""
        return self.ptz_command(ser, addr, 0x08, 0, speed)

    def move_down(self, ser, addr=1, speed=0x20):
        """Sends a command to move the camera down"""
        return self.ptz_command(ser, addr, 0x10, 0, speed)

    def move_left(self, ser, addr=1, speed=0x20):
        """Sends a command to move the camera left"""
        return self.ptz_command(ser, addr, 0x04, speed, 0)

    def move_right(self, ser, addr=1, speed=0x20):
        """Sends a command to move the camera right"""
        return self.ptz_command(ser, addr, 0x02, speed, 0)

    # --- Diagonal Combinations ---

    def move_up_right(self, ser, addr=1, p_speed=0x20, t_speed=0x20):
        """Sends a command to move the camera up and right"""
        # 0x08 (Up) | 0x02 (Right) = 0x0A
        return self.ptz_command(ser, addr, 0x0A, p_speed, t_speed)

    def move_down_left(self, ser, addr=1, p_speed=0x20, t_speed=0x20):
        """Sends a command to move the camera down and left"""
        # 0x10 (Down) | 0x04 (Left) = 0x14
        return self.ptz_command(ser, addr, 0x14, p_speed, t_speed)

    # --- Zoom Functions ---

    def zoom_in(self, ser, addr=1):
        """Sends a command to zoom in"""
        return self.ptz_command(ser, addr, 0x20, 0, 0)

    def zoom_out(self, ser, addr=1):
        """Sends a command to zoom out"""
        return self.ptz_command(ser, addr, 0x40, 0, 0)
