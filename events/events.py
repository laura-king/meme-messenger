from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from __main__ import socketio
import json, datetime
from models.message import add_message
from api.random_meme import get_random_meme


# When the client emits 'connection', this listens and executes
@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('random')
def random(data):
    print('Random message request')
    from_user = data['from_user']
    to_user = data['to_user']
    message = generate_message(from_user, to_user)
    add_message(message)
    send(message, room=from_user)
    send(message, room=to_user)
    
@socketio.on('search')
def on_search(data):
    print(data)
    print('')
    send('test message', room=data['from_user'])

@socketio.on('room')
def on_join(data):
    print(data)
    join_room(data['from_user'])
    print(data['from_user'] + ' has joined room: ' + data['from_user'])

@socketio.on('disconnect')
def disconnect(data):
    print(data['from_user'] + 'disconnected')
    leave_room(data['from_user']) 

def generate_message(from_user, to_user):
    message = {}
    message['sender'] = from_user
    message['receiver'] = to_user
    response = get_random_meme()
    link = json.loads(response.data)['url']
    message['link'] = link
    message['image'] = 'test'
    message['timestamp'] = datetime.datetime.now().strftime("%H:%M %p, %d/%m/%Y")
    
    return message