# cython: language_level=3
import cython

cpdef int map_speed(double axis_value, double deadzone=0.05) nogil:
    """
    Maps a joystick axis value to Pelco-D speed using C-level types.
    'cpdef' makes it callable from both Python and C.
    'nogil' allows it to run without the Global Interpreter Lock.
    """
    cdef double abs_val = abs(axis_value)
    cdef int scaled_speed
    
    if abs_val < deadzone:
        return 0

    # Perform math using C doubles and cast to C int
    scaled_speed = <int>((abs_val - deadzone) / (1.0 - deadzone) * 63)

    if scaled_speed < 0:
        return 0
    if scaled_speed > 63:
        return 63
    return scaled_speed