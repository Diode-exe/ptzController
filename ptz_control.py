"""PTZ Control Logic and Controller Input Handling"""

import os
import sys
import pygame
from senders import SenderFunctions
try:
    import map_speed
except ImportError:
    print("Error: Could not import map_speed module. Make sure to run compile_modules.py first.")
    print("For now, importing Python version")
    from map_speed_python import MapSpeed
    map_speed = MapSpeed().map_speed

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

        self.dpad_direction = "Neutral"

        self.hat_exist = True
        self.cam_moving = False
        self.dpad_pressed = False

        self.gui = gui_arg

        self.ser = None
        if os.name == 'nt':  # Windows
            self.sender_functions = SenderFunctions()
        else:  # Non-Windows (macOS/Linux)
            self.sender_functions = SenderFunctions(tx_port='/dev/tty.usbserial-BG02YH2O')

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
        return map_speed.map_speed(axis_value, deadzone)

    def read_inputs(self, ser_ref=None):
        """Read inputs from the controller once and update the GUI.

        This function performs a single poll of the controller and then
        re-schedules itself using `tk.after` so it doesn't block the GUI
        mainloop.
        """
        if ser_ref:
            self.ser = ser_ref
        elif self.ser is None:
            print("Serial reference not provided and self.ser is None. Cannot send commands.")
            return

        try:
            # Pygame needs to "pump" events to update the values
            pygame.event.pump()

            # 1. Read the Analog Sticks (Values are -1.0 to 1.0)
            self.ls_x = self.controller.get_axis(0)
            self.ls_y = self.controller.get_axis(1)
            self.rs_x = self.controller.get_axis(3)
            self.rs_y = self.controller.get_axis(2)

            # 2. Read the Triggers (Values are -1.0 to 1.0)
            self.lt = self.controller.get_axis(4)
            self.rt = self.controller.get_axis(5)

            # 3. Read Buttons (0 = not pressed, 1 = pressed)
            self.btn_a = self.controller.get_button(0)
            self.btn_b = self.controller.get_button(1)
            self.btn_x = self.controller.get_button(2)
            self.btn_y = self.controller.get_button(3)

            self.l_bumper = self.controller.get_button(4)
            self.r_bumper = self.controller.get_button(5)

            self.ls_click = self.controller.get_button(8)  # Left Stick Click
            self.rs_click = self.controller.get_button(9)  # Right Stick Click

            self.axes = self.controller.get_numaxes()
            self.buttons = self.controller.get_numbuttons()

            # HAT (D-pad)
            try:
                self.dpad_x, self.dpad_y = self.controller.get_hat(0)
                self.hat_exist = True
            except Exception:
                print("No HAT (D-pad) found on this controller.")
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
            if self.ls_y < -0.05:
                self.cam_moving = True
                self.sender_functions.move_up(self.ser, speed=map_speed.map_speed(self.ls_y))
            elif self.ls_y > 0.05:
                self.cam_moving = True
                self.sender_functions.move_down(self.ser, speed=map_speed.map_speed(self.ls_y))
            elif self.ls_x < -0.05:
                self.cam_moving = True
                self.sender_functions.move_left(self.ser, speed=map_speed.map_speed(self.ls_x))
            elif self.ls_x > 0.05:
                self.cam_moving = True
                self.sender_functions.move_right(self.ser, speed=map_speed.map_speed(self.ls_x))
            else:
                if self.cam_moving:
                    self.sender_functions.stop(self.ser)
                    self.cam_moving = False
            if self.lt > 0.05:
                self.cam_moving = True
                self.sender_functions.zoom_in(self.ser)
            elif self.rt > 0.05:
                self.cam_moving = True
                self.sender_functions.zoom_out(self.ser)
            else:
                if self.cam_moving:
                    self.sender_functions.stop(self.ser)
                    self.cam_moving = False
            if self.dpad_direction == "Up" and not self.dpad_pressed:
                self.dpad_pressed = True
                self.sender_functions.address += 1
            elif self.dpad_direction == "Down" and \
                self.sender_functions.address > 1 and not self.dpad_pressed:
                self.dpad_pressed = True
                self.sender_functions.address -= 1
            else:
                self.dpad_pressed = False
            if self.gui:
                # Schedule the next poll on the Tk mainloop (milliseconds)
                self.gui.root.after(50, self.read_inputs)  # ~20 Hz
            print(controller_inputs_text)  # Also print to console for non-GUI users

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
