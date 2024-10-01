import redis

def create_redis_client(host='localhost', port=6379, db=0):
    return redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

def add_client(redis_client, hostname, sid):
    redis_client.hset('clients', sid, hostname)

def remove_client(redis_client, sid):
    redis_client.hdel('clients', sid)