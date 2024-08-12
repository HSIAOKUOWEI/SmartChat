from datetime import datetime, timedelta, timezone
from .generater_keys import get_keys
from .redis_server import get_redis_client
import jwt
import os 

redis_client = get_redis_client()
algorithm = os.getenv('algorithm')
private_key, public_key = get_keys()


def encode_jwt(payload, headers=None, private_key=private_key, algorithm=algorithm):
    if headers is None:
        headers = {
            'typ': 'JWT',
            'alg': algorithm
        }
    token = jwt.encode(headers=headers, payload=payload, key=private_key, algorithm=algorithm)
    return token

def decode_jwt(token, public_key=public_key, algorithm=algorithm, verify_exp=True):
    try:
        payload = jwt.decode(token, public_key, algorithms=[algorithm], options={"verify_exp": verify_exp})
        return {"success": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token expired"}
    except jwt.InvalidTokenError:
        return {"success": False, "message": "Invalid token"}

def generate_token(user_name, user_id, token_expiration_hours = 1):
    
    # jwt由三個部分组成，以"."分割成三部分，分别是：header、payload和signature
    headers = {
        'typ': 'JWT',  # 类型，固定为JWT
        'alg': algorithm  # 算法，如：RS256、HS256等
    }

    payload = {
        'user_id': user_id,
        'user_name': user_name,
        'exp': datetime.now(timezone.utc) + timedelta(hours=token_expiration_hours), #過期時間
        'iat': datetime.now(timezone.utc) #生成時間
    }

    # 生成token
    token = encode_jwt(headers=headers, payload=payload)

    # print("private_key",private_key)
    # print("生成token",token)
    # redis保存token並設置過期時間
    redis_client.set(user_id, token, ex=token_expiration_hours * 3600)  # 3600秒 = 1小时

    return {"success":True, "token":token}

def delete_token(token):
    decoded_result = decode_jwt(token, verify_exp=False)
    if decoded_result["success"]:
        payload = decoded_result["payload"]
        redis_client.delete(payload["user_id"])
        return {"success": True, "message": "Token deleted"}, 200
    else:
        return {"success": False, "message": "Token delete failed"}, 401
    
def verify_token(token):
    decoded_result = decode_jwt(token)
    if decoded_result["success"]:
        payload = decoded_result["payload"]
        redis_token = redis_client.get(payload['user_id'])
        if redis_token is None:
            return {"success": False, "message": "Token does not exist in Redis"}

        redis_token = redis_token.decode()

        if redis_token == token:
            return {"success": True, "token": token}
        else:
            return {"success": False, "message": "Token does not exist"}
    else:
        return decoded_result

# 延長token過期時間
def refresh_token_expiry(token, 
                         token_renewal_threshold_minutes=10,
                         extension_hours=1):

    # 解码JWT令牌
    decoded_result = decode_jwt(token)
    if decoded_result["success"]:
        # 将JWT令牌中的过期时间转换为datetime对象
        exp_time = datetime.fromtimestamp(decoded_result["payload"]['exp'], timezone.utc)
        # 如果当前时间与过期时间之差小于指定的阈值（以分钟为单位）
        if exp_time - datetime.now(timezone.utc) < timedelta(minutes=token_renewal_threshold_minutes):
            # 计算新的过期时间
            new_exp = datetime.now(timezone.utc) + timedelta(hours=extension_hours)
            
            # 更新payload中的过期时间
            decoded_result["payload"]['exp'] = int(new_exp.timestamp())

            # 使用私钥重新编码JWT令牌
            new_token = encode_jwt(decoded_result["payload"])

            # 将新的JWT令牌存储到Redis中，并设置过期时间
            redis_client.set(decoded_result["payload"]["user_id"], new_token, ex=(new_exp - datetime.now(timezone.utc)).seconds)
            
            return new_token # 返回新的JWT令牌
    
    # 如果没有触发异常但也没有满足更新条件，则返回None
    return None
if __name__ == '__main__':
    token = generate_token("2342342432")
    print(token)
    payload = verify_token(token["token"])
    print(payload)

    print(redis_client.keys("*"))
    delete_token(payload["token"])
    print(redis_client.keys("*"))