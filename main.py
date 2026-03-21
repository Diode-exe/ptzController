import pygame
import time

class PTZControl:
    def __init__(self):
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
        try:
            while True:
                # Pygame needs to "pump" events to update the values
                pygame.event.pump()

                # 1. Read the Analog Sticks (Values are -1.0 to 1.0)
                # Left Stick: Axis 0 (X), Axis 1 (Y)
                # Right Stick: Axis 3 (X), Axis 4 (Y)
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

                # print(self.controller.get_hat(0), end="\r")

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

                # if self.btn_a:
                #     self.controller.rumble(0, 1, 50)  # rumble(left_motor, right_motor, duration_ms)

                # print(self.controller.get_numhats(), end="\r")

                # Clear the line and print the values
                # print(f"LS: ({ls_x:>5.2f}, {ls_y:>5.2f}) | RS: ({rs_x:>5.2f}, {rs_y:>5.2f}) | A: {btn_a}", end="\r")
                print(f"Axes: {self.axes} | Buttons: {self.buttons} | LS: ({self.ls_x:>5.2f}, {self.ls_y:>5.2f}) | RS: ({self.rs_x:>5.2f}, {self.rs_y:>5.2f}) | LT: {self.lt:>5.2f} | RT: {self.rt:>5.2f} | A: {self.btn_a} | B: {self.btn_b} | X: {self.btn_x} | Y: {self.btn_y} | LB: {self.l_bumper} | RB: {self.r_bumper} | LS Click: {self.ls_click} | RS Click: {self.rs_click} | DPad: {self.dpad_direction}", end="\r")

                time.sleep(0.05) # Update 20 times per second

        except KeyboardInterrupt:
            print("\nStopping...")
            pygame.quit()

    # def threaded_read_inputs(self):
    #     input_thread = threading.Thread(target=self.read_inputs, daemon=True)
    #     input_thread.start()

if __name__ == "__main__":
    ptz_control = PTZControl()
    ptz_control.read_inputs()
    while True:
        time.sleep(1)
