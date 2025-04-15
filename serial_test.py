import serial

ser = serial.Serial('COM6', 9600)  # Replace 'COM3' with your actual port
print(ser.name)
ser.close()