default ={ "default_user":{"id": "123",
                           "username": "admin",
                           "password": "password"}
                           }



class User:
    def __init__(self, user_id,user_name, ):
        self.id = user_id
        self.name = user_name

    @staticmethod
    def check_credentials(username, password):
        # 簡單的預設賬密
        if username == default["default_user"]["username"] and password == default["default_user"]["password"]:

            return User(user_id = default["default_user"]["id"], user_name=default["default_user"]["username"])
        return None