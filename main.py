import pygame
import time

# Initialize Pygame and the Joystick system
pygame.init()
pygame.joystick.init()

# Check if a controller is actually plugged in
if pygame.joystick.get_count() == 0:
    print("No controller found! Plug it in and try again.")
    exit()

# Connect to the first controller
controller = pygame.joystick.Joystick(0)
controller.init()

print(f"Connected to: {controller.get_name()}")

try:
    while True:
        # Pygame needs to "pump" events to update the values
        pygame.event.pump()

        # 1. Read the Analog Sticks (Values are -1.0 to 1.0)
        # Left Stick: Axis 0 (X), Axis 1 (Y)
        # Right Stick: Axis 3 (X), Axis 4 (Y)
        ls_x = controller.get_axis(0)
        ls_y = controller.get_axis(1)
        rs_x = controller.get_axis(3)
        rs_y = controller.get_axis(2)

        # 2. Read the Triggers (Values are -1.0 to 1.0)
        lt = controller.get_axis(4)
        rt = controller.get_axis(5)

        # 3. Read Buttons (0 = not pressed, 1 = pressed)
        btn_a = controller.get_button(0)
        btn_b = controller.get_button(1)
        btn_x = controller.get_button(2)
        btn_y = controller.get_button(3)

        l_bumper = controller.get_button(4)
        r_bumper = controller.get_button(5)

        ls_click = controller.get_button(8)  # Left Stick Click
        rs_click = controller.get_button(9)  # Right Stick Click

        axes = controller.get_numaxes()
        buttons = controller.get_numbuttons()

        # print(controller.get_hat(0), end="\r")

        dpad_x, dpad_y = controller.get_hat(0)

        if dpad_x == -1:
            dpad_direction = "Left"
        elif dpad_x == 1:
            dpad_direction = "Right"
        elif dpad_y == -1:
            dpad_direction = "Down"
        elif dpad_y == 1:
            dpad_direction = "Up"
        else:
            dpad_direction = "Neutral"

        # print(controller.get_numhats(), end="\r")

        # Clear the line and print the values
        # print(f"LS: ({ls_x:>5.2f}, {ls_y:>5.2f}) | RS: ({rs_x:>5.2f}, {rs_y:>5.2f}) | A: {btn_a}", end="\r")
        print(f"Axes: {axes} | Buttons: {buttons} | LS: ({ls_x:>5.2f}, {ls_y:>5.2f}) | RS: ({rs_x:>5.2f}, {rs_y:>5.2f}) | LT: {lt:>5.2f} | RT: {rt:>5.2f} | A: {btn_a} | B: {btn_b} | X: {btn_x} | Y: {btn_y} | LB: {l_bumper} | RB: {r_bumper} | LS Click: {ls_click} | RS Click: {rs_click} | DPad: {dpad_direction}", end="\r")

        time.sleep(0.05) # Update 20 times per second

except KeyboardInterrupt:
    print("\nStopping...")
    pygame.quit()