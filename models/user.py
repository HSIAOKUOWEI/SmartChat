default ={ "default_user":{"username": "admin",
                           "password": "password"}
                           }



class User:
    def __init__(self, user_name, ):
        self.name = user_name

    @staticmethod
    def check_credentials(username, password):
        # 簡單的預設賬密
        if username == default["default_user"]["username"] and password == default["default_user"]["password"]:

            return {"success":True, "user_name": username}
        else:
            return {"success":False, "user_name": username}