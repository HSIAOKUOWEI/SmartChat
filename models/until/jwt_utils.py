from .generater_keys import get_keys
from ..config import algorithm
import jwt
from datetime import datetime, timedelta, timezone
from .redis_server import get_redis_client

redis_client = get_redis_client()
private_key, public_key = get_keys()

def generate_token(user_id, token_expiration_hours = 1):
    
    # jwt由三個部分组成，以"."分割成三部分，分别是：header、payload和signature
    headers = {
        'typ': 'JWT',  # 类型，固定为JWT
        'alg': algorithm  # 算法，如：RS256、HS256等
    }

    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=token_expiration_hours), #過期時間
        'iat': datetime.now(timezone.utc) #生成時間
    }

    # 生成token
    token = jwt.encode(headers=headers, payload=payload,
                       key=private_key, algorithm=algorithm
                       )
    # print("private_key",private_key)
    # print("生成token",token)
    # redis保存token並設置過期時間
    redis_client.set(user_id, token, ex=token_expiration_hours * 3600)  # 3600秒 = 1小时

    return {"success":True, "token":token}
def delete_token(token):
    try:
        payload = jwt.decode(token, public_key, algorithms=[algorithm], options={"verify_exp": False})
        redis_client.delete(payload["user_id"])
        return {"success":True, "message": "Token deleted"}, 200
    except jwt.InvalidTokenError:
        return {"success":False, "message": "Token delete failed"}, 401
    
def verify_token(token):
    try:
        # 先取出解密後數據
        payload = jwt.decode(token, public_key, algorithms=[algorithm])

        # 檢查 Redis 中是否存在該 token
        redis_token = redis_client.get(payload['user_id'])
        
        if redis_token is None:
            return {"success": False, "message": "Token does not exist in Redis"}

        # Decode Redis token and compare
        redis_token = redis_token.decode()
        # 檢查 token 是否有效
        if redis_token == token:
            print("成功")
            return {"success":True , "token": token}
        
        else:
            print("失敗")
            return {"success":False , "message": "Token does not exist"}

    except jwt.ExpiredSignatureError:
        # token已過期
        return {"success":False, "message": "Token expired"}
    except jwt.InvalidTokenError:
        # 無效的token
        return {"success":False, "message": "Invalid token"}

# 延長token過期時間
def refresh_token_expiry(token, 
                         token_renewal_threshold_minutes=10,
                         extension_hours=1):
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, public_key, algorithms=[algorithm], options={"verify_exp": False})
       
        # 将JWT令牌中的过期时间转换为datetime对象
        exp_time = datetime.fromtimestamp(payload['exp'], timezone.utc)
       
        # 如果当前时间与过期时间之差小于指定的阈值（以分钟为单位）
        if exp_time - datetime.now(timezone.utc) < timedelta(minutes=token_renewal_threshold_minutes):
            # 计算新的过期时间
            new_exp = datetime.now(timezone.utc) + timedelta(hours=extension_hours)
            
            # 更新payload中的过期时间
            payload['exp'] = int(new_exp.timestamp())

            # 使用私钥重新编码JWT令牌
            new_token = jwt.encode(payload, private_key, algorithm=algorithm)

            # 将新的JWT令牌存储到Redis中，并设置过期时间
            redis_client.set(payload["user_id"], new_token, ex=(new_exp - datetime.now(timezone.utc)).seconds)
            return new_token # 返回新的JWT令牌
    
     # 如果解码JWT令牌时发生异常（例如，令牌无效）
    except jwt.InvalidTokenError:
        return None
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