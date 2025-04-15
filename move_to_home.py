import serial
import argparse
import threading
from time import sleep
import math
import json

def read_serial():
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')
    
ser = None  # Declare at module level

def connect_serial(port):
    global ser
    if ser is None or not ser.is_open:
        print(f"Connecting to {port}...")
        ser = serial.Serial(port, baudrate=115200, dsrdtr=None)
        ser.setRTS(False)
        ser.setDTR(False)

def send_to_home():
    if ser is None or not ser.is_open:
        raise RuntimeError("Serial port not open.")
    
    # Replace this with your actual home coordinates
    home_coord = json.dumps({'T': 1041, 'x': 100, 'y': 100, 'z': 200})
    ser.write(home_coord.encode() + b'\n')
    print(f"Sent home: {home_coord}")
    
# Not to be run as main except for testing purposes 
if __name__ == "__main__":
    # Connect once when the server starts
    try:
        connect_serial('COM6')  # or 'COM3' on Windows
    except Exception as e:
        print(f"Error connecting to robot arm: {e}")
        
    send_to_home()