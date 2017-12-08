from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from __main__ import socketio
import json


# When the client emits 'connection', this listens and executes
@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('random')
def random(data):
    print('Random message request')
    from_user = data['from_user']
    to_user = data['to_user']
    
@socketio.on('search')
def on_search(data):
    print(data)
    
    send('test message', room=data['from_user'])

@socketio.on('room')
def on_join(data):
    print(data)
    join_room(data['from_user'])
    print(data['from_user'] + 'has joined room: ' + data['from_user'])
    


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
