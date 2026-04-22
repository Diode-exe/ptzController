from flask import Flask, render_template, request
import serial
from serial_port import DummySerial  # Import the dummy serial for testing

# dummy_serial = DummySerial('COM_MOCK', 9600)  # Use the dummy serial for testing

app = Flask(__name__)

# Replace with your actual Mac USB path (run 'ls /dev/cu.*' to find it)
SERIAL_PORT = 'COM3'
ser = DummySerial(SERIAL_PORT, 9600)  # Use the dummy serial for testing

def send_pelco(cmd2, p_speed=0x20, t_speed=0x00):
    packet = bytearray([0xFF, 0x01, 0x00, cmd2, p_speed, t_speed])
    checksum = sum(packet[1:]) % 256
    packet.append(checksum)
    ser.write(packet)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cmd/<action>')
def command(action):
    # Logic for different button presses
    if action == 'left':   send_pelco(0x04, 0x20, 0x00)
    elif action == 'right': send_pelco(0x02, 0x20, 0x00)
    elif action == 'up':    send_pelco(0x08, 0x00, 0x20)
    elif action == 'down':  send_pelco(0x10, 0x00, 0x20)
    elif action == 'stop':  send_pelco(0x00, 0x00, 0x00)
    return f"OK: {action}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)