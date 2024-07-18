from flask import Flask, render_template, jsonify
import serial
import threading
import time

app = Flask(__name__)

# Update the serial port to match the correct one identified in Device Manager
ser = serial.Serial('COM3', 9600, timeout=1)  # Change 'COM4' to your correct serial port

parking_status = "EMPTY"

def read_from_serial():
    global parking_status
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Received line: {line}")  # For debugging purposes
            if "FULL" in line:
                parking_status = "FULL"
            elif "EMPTY" in line:
                parking_status = "EMPTY"
        time.sleep(0.1)  # Adjust the sleep duration as needed

@app.route('/')
def index():
    return render_template('index.html', parking_status=parking_status)

@app.route('/status')
def status():
    return jsonify(parking_status=parking_status)

if __name__ == '__main__':
    # Start serial reading in a separate thread
    thread = threading.Thread(target=read_from_serial)
    thread.daemon = True
    thread.start()

    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000)
