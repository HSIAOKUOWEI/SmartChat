import redis
from ..config import redis_ip, redis_port, redis_db


def get_redis_client(ip: str = redis_ip, port: int = redis_port, db: int = redis_db):
    return redis.StrictRedis(host=redis_ip, port=redis_port, db=redis_db)

