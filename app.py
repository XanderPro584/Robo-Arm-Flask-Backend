from flask import Flask, send_from_directory, request, jsonify
import os
from move_to_home import connect_serial, send_to_home, get_pos, move_left, move_right, move_to_joy_pos
import json


# Path to React's build folder
BUILD_DIR = os.path.join(os.path.dirname(__file__), '../frontend/build')

app = Flask(__name__, static_folder=BUILD_DIR, static_url_path='')

# Connect once when the server starts
try:
    connect_serial('COM6')  # or 'COM3' on Windows
except Exception as e:
    print(f"Error connecting to robot arm: {e}")
  
# Serve the React index.html for the base URL
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve any other static files (JS, CSS, etc.)  
@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        # Fallback for React Router: serve index.html
        return send_from_directory(app.static_folder, 'index.html')
        
@app.route('/api/home')
def home():
    try:
        send_to_home()
        return jsonify({'status': 'Arm sent to home position'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/api/position')
def get_position():
    current_position = get_pos()
    return jsonify(current_position)

@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.json
    x = data['x']
    y = data['y']
    print(f"Joystick moved to: x={x}, y={y}")
    move_to_joy_pos(x, y)
    return {'status': 'received'}

@app.route('/api/left')
def go_left():
    try:
        # Replace with your actual command to move left
        move_left()
        return jsonify({'status': 'Arm moved left'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/right')
def go_right():
    try:
        # Replace with your actual command to move left
        move_right()
        return jsonify({'status': 'Arm moved right'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=False)
