import socketio

from ops.socketio_module import sio

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
