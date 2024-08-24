import redis
import os
redis_ip = os.getenv('REDIS_IP')
redis_port = int(os.getenv('REDIS_PORT'))
redis_timeout = int(os.getenv('REDIS_TIMEOUT', 5000))  # 連接超時，單位為毫秒

def get_redis_client(ip: str = redis_ip, port: int = redis_port, timeout: int = redis_timeout):
    try:
        client = redis.StrictRedis(host=ip, port=port)
        client.ping()  # 尝试连接
        return client
    except (redis.ConnectionError, redis.TimeoutError) as e:
        client = redis.StrictRedis(host="localhost", port=port)
        client.ping()  # 尝试连接
        return client

