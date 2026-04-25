"""PTZ Controller"""

# import tkinter as tk
# import threading
from ptz_control import PTZControl

# class GUI:
#     """Graphical User Interface for displaying controller inputs."""
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("PTZ Controller")

#         self.root.geometry("1000x100")

#         self.controller_inputs_var = tk.StringVar()
#         self.controller_inputs_var.set("Controller Inputs will be displayed here.")

#         self.controller_inputs = tk.Label(self.root, textvariable=self.controller_inputs_var)
#         self.controller_inputs.pack(padx=20, pady=20)

#     def run(self):
#         """Start the GUI event loop."""
#         self.root.mainloop()

#     def threaded_read_inputs(self):
#         """Start the controller input reading in a separate thread."""
#         input_thread = threading.Thread(target=ptz_control.read_inputs, daemon=True)
#         input_thread.start()

if __name__ == "__main__":
    # gui = GUI()

    # ptz_control = PTZControl(gui)
    ptz_control = PTZControl()
    # ptz_control.read_inputs()
    # gui.threaded_read_inputs()

    # gui.run()
    while True:
        ptz_control.read_inputs()
