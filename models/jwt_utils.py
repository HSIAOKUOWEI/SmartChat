import jwt
import datetime
from .redis_server_setting import *

SECRET_KEY = '123'  # 请使用更安全的密钥
algorithm = 'HS256'



def generate_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # token有效期为1小时
    }
    # 生成token
    token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)

    # 存储token到Redis并设置过期时间
    redis_client.set(token, user_id, ex=3600)  # 3600秒 = 1小时

    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        user_id = payload['user_id']

        # 从Redis中查找token
        if redis_client.exists(token):
            print("Token found in Redis")
            return user_id, payload
        else:
            print("Token not found in Redis or expired")
            return None, None  # token在Redis中不存在或已过期
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None, None  # token过期
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None, None  # 无效的toke
