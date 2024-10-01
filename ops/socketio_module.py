import time

import socketio
from ops.kafka_module import create_producer, create_consumer
from ops.redis_module import create_redis_client, add_client, remove_client

sio = socketio.Server( cors_allowed_origins="*")
redis_client = create_redis_client()
producer = create_producer(['127.0.0.1:19092'])
consumer = create_consumer(['127.0.0.1:19092'], 'my_topic')

@sio.event
def connect(sid, environ):
    hostname = environ['REMOTE_ADDR']
    add_client(redis_client, hostname, sid)
    print(f'Client {hostname} connected with SID {sid}')

@sio.event
def disconnect(sid):
    remove_client(redis_client, sid)
    print(f'Client with SID {sid} disconnected')

@sio.event
def save_payload(sid, data):
    producer.send('my_topic', data)
    print(f'Payload saved to Kafka: {data}')

def consume_and_broadcast():
    print("Ma lansez!!!!")
    while True:
        try:
            message = consumer.poll(10.0)
            if not message:
                time.sleep(5)
            print(f'Received message: {message}')
        except:
            pass
        finally:
            consumer.close()
            print("La revedere")

        print(f'new_message {message.value}')
        for sid in redis_client.hkeys('clients'):
            sio.emit('new_message', message.value, room=sid)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    sio.start_background_task(consume_and_broadcast())
    #eventlet.spawn(consume_and_broadcast)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
