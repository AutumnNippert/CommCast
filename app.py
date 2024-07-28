from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
CHAT_FILE = 'chat.json'

# Ensure the chat file exists
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, 'w') as file:
        json.dump([], file)

# Helper function to read chat messages from the JSON file
def read_chat():
    with open(CHAT_FILE, 'r') as file:
        return json.load(file)

# Helper function to write chat messages to the JSON file
def write_chat(messages):
    with open(CHAT_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = read_chat()
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def add_message():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    new_message = request.get_json()
    messages = read_chat()
    messages.append(new_message)
    write_chat(messages)
    socketio.emit('new_message', new_message)
    return jsonify(new_message), 201

if __name__ == '__main__':
    # run on 10.132.200.7:5000
    socketio.run(app, host='10.132.200.7', port=5000)
