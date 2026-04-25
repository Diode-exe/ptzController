"""PTZ Control Logic and Controller Input Handling"""

import sys
import pygame
import serial
from senders import SenderFunctions

class PTZControl:
    """Class to handle PTZ control logic and read controller inputs."""
    def __init__(self, gui_arg=None):
        self.controller = None
        self.ls_x = 0.0
        self.ls_y = 0.0
        self.rs_x = 0.0
        self.rs_y = 0.0

        self.lt = 0.0
        self.rt = 0.0

        self.btn_a = 0
        self.btn_b = 0
        self.btn_x = 0
        self.btn_y = 0

        self.l_bumper = 0
        self.r_bumper = 0

        self.ls_click = 0
        self.rs_click = 0

        self.axes = 0
        self.buttons = 0

        self.dpad_x = 0
        self.dpad_y = 0

        self.hat_exist = False

        self.dpad_direction = "Neutral"

        self.gui = gui_arg

        self.sender_functions = SenderFunctions()

        # Initialize Pygame and the Joystick system
        pygame.init()
        pygame.joystick.init()

        # Check if a controller is actually plugged in
        if pygame.joystick.get_count() == 0:
            print("No controller found! Plug it in and try again.")
            sys.exit()

        # Connect to the first controller
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        print(f"Connected to: {self.controller.get_name()}")

    def map_speed(self, axis_value, deadzone=0.05):
        """Maps a joystick axis value (-1.0 to 1.0) to a Pelco-D speed (0 to 63) with a deadzone."""
        # If the stick is only moved slightly, return 0 to prevent "creep"
        if abs(axis_value) < deadzone:
            return 0

        # Scale the remaining 0.1 -> 1.0 range to 0 -> 63
        # This ensures that once you pass the deadzone, you start at speed 1
        scaled_speed = int((abs(axis_value) - deadzone) / (1.0 - deadzone) * 63)

        return max(0, min(scaled_speed, 63))

    def read_inputs(self):
        """Read inputs from the controller once and update the GUI.

        This function performs a single poll of the controller and then
        re-schedules itself using `tk.after` so it doesn't block the GUI
        mainloop.
        """
        try:
            # Pygame needs to "pump" events to update the values
            pygame.event.pump()

            # 1. Read the Analog Sticks (Values are -1.0 to 1.0)
            self.ls_x = self.controller.get_axis(0)
            self.ls_y = self.controller.get_axis(1)
            self.rs_x = self.controller.get_axis(3)
            self.rs_y = self.controller.get_axis(2)
            print("Got axes...")

            # 2. Read the Triggers (Values are -1.0 to 1.0)
            self.lt = self.controller.get_axis(4)
            self.rt = self.controller.get_axis(5)
            print("Got triggers...")

            # 3. Read Buttons (0 = not pressed, 1 = pressed)
            self.btn_a = self.controller.get_button(0)
            self.btn_b = self.controller.get_button(1)
            self.btn_x = self.controller.get_button(2)
            self.btn_y = self.controller.get_button(3)
            print("Got buttons...")

            self.l_bumper = self.controller.get_button(4)
            self.r_bumper = self.controller.get_button(5)
            print("Got bumpers...")

            self.ls_click = self.controller.get_button(8)  # Left Stick Click
            self.rs_click = self.controller.get_button(9)  # Right Stick Click
            print("Got stick clicks...")

            self.axes = self.controller.get_numaxes()
            self.buttons = self.controller.get_numbuttons()
            print("Got counts...")

            # HAT (D-pad)
            try:
                self.dpad_x, self.dpad_y = self.controller.get_hat(0)
                self.hat_exist = True
            except Exception:
                self.dpad_x, self.dpad_y = 0, 0
                self.hat_exist = False
            if self.hat_exist:
                if self.dpad_x == -1:
                    self.dpad_direction = "Left"
                elif self.dpad_x == 1:
                    self.dpad_direction = "Right"
                elif self.dpad_y == -1:
                    self.dpad_direction = "Down"
                elif self.dpad_y == 1:
                    self.dpad_direction = "Up"
                else:
                    self.dpad_direction = "Neutral"

            controller_inputs_text = (
                f"Axes: {self.axes} | Buttons: {self.buttons} "
                f"| LS: ({self.ls_x:>5.2f}, {self.ls_y:>5.2f})"
                f"| RS: ({self.rs_x:>5.2f}, {self.rs_y:>5.2f})"
                f"| LT: {self.lt:>5.2f} | RT: {self.rt:>5.2f} "
                f"| A: {self.btn_a} | B: {self.btn_b}"
                f"| X: {self.btn_x} | Y: {self.btn_y} "
                f"| LB: {self.l_bumper} | RB: {self.r_bumper} "
                f"| LS Click: {self.ls_click} | RS Click: {self.rs_click} "
                f"| DPad: {self.dpad_direction} | Address: {self.sender_functions.address} "
            )
            if self.gui:
                self.gui.controller_inputs_var.set(controller_inputs_text)
            with serial.Serial(self.sender_functions.tx_port,
                               self.sender_functions.baud_rate, timeout=1) as ser:
                if self.ls_y < -0.5:
                    self.sender_functions.move_up(ser, speed=self.map_speed(self.ls_y))
                elif self.ls_y > 0.5:
                    self.sender_functions.move_down(ser, speed=self.map_speed(self.ls_y))
                elif self.ls_x < -0.5:
                    self.sender_functions.move_left(ser, speed=self.map_speed(self.ls_x))
                elif self.ls_x > 0.5:
                    self.sender_functions.move_right(ser, speed=self.map_speed(self.ls_x))
                else:
                    self.sender_functions.stop(ser)
                if self.lt > 0.5:
                    self.sender_functions.zoom_in(ser)
                elif self.rt > 0.5:
                    self.sender_functions.zoom_out(ser)
                if self.dpad_direction == "Up":
                    self.sender_functions.address += 1
                elif self.dpad_direction == "Down" and self.sender_functions.address > 1:
                    self.sender_functions.address -= 1

            # Schedule the next poll on the Tk mainloop (milliseconds)
            if self.gui:
                self.gui.root.after(50, self.read_inputs)  # ~20 Hz

        except Exception as e:
            print("Error reading inputs:", e)
            try:
                pygame.quit()
            except Exception:
                pass
            # If GUI exists, close it to stop the app
            if self.gui:
                try:
                    self.gui.root.quit()
                except Exception:
                    pass
