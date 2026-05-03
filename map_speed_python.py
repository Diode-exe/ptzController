class MapSpeed:
    """Class to map joystick axis values to Pelco-D speed values."""
    def __init__(self):
        pass

    def map_speed(self, axis_value, deadzone=0.05):
        """Maps a joystick axis value (-1.0 to 1.0) to a Pelco-D speed (0 to 63) with a deadzone."""
        # If the stick is only moved slightly, return 0 to prevent "creep"
        if abs(axis_value) < deadzone:
            return 0

        # Scale the remaining 0.1 -> 1.0 range to 0 -> 63
        # This ensures that once you pass the deadzone, you start at speed 1
        scaled_speed = int((abs(axis_value) - deadzone) / (1.0 - deadzone) * 63)

        return max(0, min(scaled_speed, 63))
