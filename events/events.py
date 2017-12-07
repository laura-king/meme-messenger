from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room
from __main__ import socketio

# When the client emits 'connection', this listens and executes
@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
