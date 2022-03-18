from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import os
 
async_mode = None
app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
 
## Used by App Service For linux
PORT = os.environ["PORT"]
serverIP = "0.0.0.0"
 
# # Used by Local debug.
# PORT = 5000
# serverIP = "127.0.0.1"
 
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
 
@socketio.on('my_event', namespace='/test')
def test_message(message):
    print('receive message:' + message['data'],)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})
 
@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print('broadcast message:' + message['data'],)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
 
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)
 
if __name__ == '__main__':
    socketio.run(app,port=PORT, host=serverIP, debug=True)
    print('socket io start')