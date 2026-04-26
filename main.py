"""PTZ Controller"""

import os
import serial
from ptz_control import PTZControl

class GlobalClass:
    """A class to hold global variables and references."""
    def __init__(self):
        self.is_on_windows = False
        self.ptz_control = None

if os.name == 'nt':  # Windows
    import tkinter as tk
    import threading
    class GUI:
        """Graphical User Interface for displaying controller inputs."""
        def __init__(self, global_class_ref):
            self.global_class = global_class_ref
            self.root = tk.Tk()
            self.root.title("PTZ Controller")

            self.root.geometry("1000x100")

            self.controller_inputs_var = tk.StringVar()
            self.controller_inputs_var.set("Controller Inputs will be displayed here.")

            self.controller_inputs = tk.Label(self.root, textvariable=self.controller_inputs_var)
            self.controller_inputs.pack(padx=20, pady=20)

        def run(self):
            """Start the GUI event loop."""
            self.root.mainloop()

        def threaded_read_inputs(self):
            """Start the controller input reading in a separate thread."""
            input_thread = threading.Thread(target=self.global_class.ptz_control.read_inputs,
                                            daemon=True)
            input_thread.start()

else:
    print("Non-Windows platform detected. Running without GUI.")
    # On non-Windows platforms, we won't initialize the GUI
    # because pygame on macOS (maybe fault of pygame, maybe fault of macOS, don't know)
    # has issues with threading
    # I think it's because of the Cocoa framework,
    # but I haven't fully investigated yet.
    # The macOS version will just print controller inputs and commands to the console.
    # don't know if Linux has the same issue but I haven't tested it yet so we'll see
    # For now, non-Windows users will just have a console-based experience without the GUI,
    # but it should still work fine for sending commands to the camera.

if __name__ == "__main__":
    global_class = GlobalClass()
    if os.name == 'nt':
        global_class.is_on_windows = True
        gui = GUI(global_class)

        global_class.ptz_control = PTZControl(gui_arg=gui)
        # ptz_control.read_inputs()
        gui.threaded_read_inputs()

        gui.run()
    else:
        global_class.ptz_control = PTZControl(gui_arg=None)
        with serial.Serial(global_class.ptz_control.sender_functions.tx_port,
                    global_class.ptz_control.sender_functions.baud_rate, timeout=1) as ser:
            while True:
                global_class.ptz_control.read_inputs(ser_ref=ser)
