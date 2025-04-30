import serial
import argparse
import threading
from time import sleep
import math
import json

ser = None  # Declare at module level
current_position = {'x': 0, 'y': 0, 'z': 0}  # Initialize current position
virtual_position = {'x': 0, 'y': 0, 'z': 0}  # Initialize virtual position

def read_serial():
    global current_position
    while True:
        try: 
            data = ser.readline().decode('utf-8').strip()
            if data: 
                # print(f"Received: {data}")
                    
                json_data = json.loads(data)
                if all(k in json_data for k in ('x', 'y', 'z')):
                    current_position.update({
                        'x': json_data['x'],
                        'y': json_data['y'],
                        'z': json_data['z']
                    })
        except Exception as e:
            print(f"Error reading serial data: {e}")

def connect_serial(port):
    global ser
    if ser is None or not ser.is_open:
        print(f"Connecting to {port}...")
        ser = serial.Serial(port, baudrate=115200, dsrdtr=None)
        ser.setRTS(False)
        ser.setDTR(False)
        threading.Thread(target=read_serial, daemon=True).start()

def send_to_home():
    if ser is None or not ser.is_open:
        raise RuntimeError("Serial port not open.")
    
    # Replace this with your actual home coordinates
    home_coord = json.dumps({'T': 1041, 'x': 100, 'y': 100, 'z': 200})

    ser.write(home_coord.encode() + b'\n')
    print(f"Sent home: {home_coord}")
    
    virtual_position['x'] = 100
    virtual_position['y'] = 100
    virtual_position['z'] = 200
    
def get_pos():
    command = {"T":105}
    command = json.dumps(command)
    ser.write(command.encode() + b'\n')
    return current_position

def move_left():
    command = {'T': 1041, 'x': virtual_position['x'] - 100, 'y': virtual_position['y'], 'z': virtual_position['z']}
    command = json.dumps(command)
    ser.write(command.encode() + b'\n')
    print(f"Sent move left: {command}")
    virtual_position['x'] -= 100
    
def move_right():
    command = {'T': 1041, 'x': virtual_position['x'] + 100, 'y': virtual_position['y'], 'z': virtual_position['z']}
    command = json.dumps(command)
    ser.write(command.encode() + b'\n')
    print(f"Sent move right : {command}")
    virtual_position['x'] += 100
    
def move_to_joy_pos(x, y):
    virtual_position['x'] = x * 3
    virtual_position['y'] = y * 3
    # if -300 < virtual_position['x'] + x < 300:
    #     virtual_position['x'] = virtual_position['x'] + x
        
    # else:
    #     if virtual_position['x'] + x < -300:
    #         virtual_position['x'] = -300
            
    #     elif virtual_position['x'] + x > 300:
    #         virtual_position['x'] = 300
            
    #     print(f"Joystick position out of bounds: x={virtual_position['x']}, y={virtual_position['y']}")


    # if -300 < virtual_position['y'] + y < 300:
    #     virtual_position['y'] = virtual_position['y'] + y
        
    # else:      
    #     if virtual_position['y'] + y < -300:
    #         virtual_position['y'] = -300
        
    #     elif virtual_position['y'] + y > 300:
    #         virtual_position['y'] = 300
    #     print(f"Joystick position out of bounds: x={virtual_position['x']}, y={virtual_position['y']}")

              
    command= {'T': 1041, 'x': virtual_position['x'], 'y': virtual_position['y'], 'z': virtual_position['z']}
    command = json.dumps(command)
    ser.write(command.encode() + b'\n')
    print(f"Sent move to joystick position: {command}")
          

    
    
    
    
# Not to be run as main except for testing purposes 
if __name__ == "__main__":
    # Connect once when the server starts
    try:
        connect_serial('COM6')  # or 'COM3' on Windows
    except Exception as e:
        print(f"Error connecting to robot arm: {e}")
        
    send_to_home()