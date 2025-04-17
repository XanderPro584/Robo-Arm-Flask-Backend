from flask import Flask, send_from_directory, request, jsonify
import os
from move_to_home import connect_serial, send_to_home


# Path to React's build folder
BUILD_DIR = os.path.join(os.path.dirname(__file__), '../frontend/build')

app = Flask(__name__, static_folder=BUILD_DIR, static_url_path='')

# Connect once when the server starts
try:
    connect_serial('COM6')  # or 'COM3' on Windows
except Exception as e:
    print(f"Error connecting to robot arm: {e}")
    
current_position = {'x':1, 'y':2, 'z':3}
    
@app.route('/api/home')
def home():
    try:
        send_to_home()
        return jsonify({'status': 'Arm sent to home position'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    
    
    
@app.route('/api/position')
def get_position():
    return jsonify(current_position)

if __name__ == '__main__':
    app.run(debug=False)
