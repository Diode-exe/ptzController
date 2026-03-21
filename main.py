"""PTZ Controller"""

import tkinter as tk
import pygame

class GUI:
    """Graphical User Interface for displaying controller inputs."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PTZ Controller")

        self.controller_inputs_var = tk.StringVar()
        self.controller_inputs_var.set("Controller Inputs will be displayed here.")

        self.controller_inputs = tk.Label(self.root, textvariable=self.controller_inputs_var)
        self.controller_inputs.pack(padx=20, pady=20)

    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()

class PTZControl:
    """Class to handle PTZ control logic and read controller inputs."""
    def __init__(self, gui_arg):
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

        self.gui = gui_arg

        # Initialize Pygame and the Joystick system
        pygame.init()
        pygame.joystick.init()

        # Check if a controller is actually plugged in
        if pygame.joystick.get_count() == 0:
            print("No controller found! Plug it in and try again.")
            exit()

        # Connect to the first controller
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        print(f"Connected to: {self.controller.get_name()}")

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
            self.dpad_x, self.dpad_y = self.controller.get_hat(0)

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
                f"| DPad: {self.dpad_direction}"
            )
            self.gui.controller_inputs_var.set(controller_inputs_text)

            # Schedule the next poll on the Tk mainloop (milliseconds)
            self.gui.root.after(50, self.read_inputs)  # ~20 Hz

        except Exception as e:
            print("Error reading inputs:", e)
            try:
                pygame.quit()
            except Exception:
                pass
            # If GUI exists, close it to stop the app
            try:
                self.gui.root.quit()
            except Exception:
                pass

    # def threaded_read_inputs(self):
    #     input_thread = threading.Thread(target=self.read_inputs, daemon=True)
    #     input_thread.start()

if __name__ == "__main__":
    gui = GUI()

    ptz_control = PTZControl(gui)
    ptz_control.read_inputs()

    gui.run()
