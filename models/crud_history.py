from .until.mongodb_server import get_mongodb_db
from datetime import datetime, timezone
from .until.jwt_utils import decode_jwt
from bson import ObjectId


db = get_mongodb_db()

users_collection = db.users


# 儲存對話内容的邏輯如下：
# 前端發送消息，後端處理完之後，就會來到儲存消息的邏輯
# 如果對話框id不為空，就代表是在已有對話框上進行聊天的，我們只需要直接根據user_id和對話框id，去消息表中已有的記錄中新增這次的數據即可
# 如果對話框id為空，就代表是新建的對話框，我們需要先在對話框表中新增一個對話框，拿到這個新的對話框id，再去消息表中插入相關數據
# 因為新增的對話框沒有標題，所以再插入之前我們會調用一個函數，去根據聊天記錄生成對話框標題，再插入消息表中
# 兩個插入和新增邏輯完成之後都會返回對話框id給前端，前端再將對話框id存起來，下次聊天時就可以直接使用這個對話框id了

# 根据token获取用户id的函数
def get_user_id(token):
    decode_result = decode_jwt(token=token)
    user_id = decode_result["payload"].get("user_id")
    if not user_id:
        username = decode_result["payload"]["user_name"]
        user = users_collection.find_one({'account': username})
        if user:
            user_id = str(user['_id'])
        else:
            raise Exception('User not found')
    return user_id

# 對話框表
class Dialogue:
    def __init__(self):
        self.collection = db['dialogues']

    def generate_title(self, messages):
        import random
        import uuid
        # 生成標題
        random_number = random.randint(1, 100)  # 生成1到100之間的隨機數
        unique_id = uuid.uuid4()  # 生成一個唯一的UUID
        title = f"Generated Title {random_number} - {unique_id}"
        return title

    def create_dialogue(self, user_id, title=""):
        # 創建新的對話框
        dialogue = {
            "user_id": ObjectId(user_id), # 用戶id
            "title": title, # 標題默認為空
            "created_at": datetime.now(timezone.utc), # 創建時間
            "updated_at": datetime.now(timezone.utc) # 最後使用時間
        }
        result = self.collection.insert_one(dialogue)
        return str(result.inserted_id)

    def update_dialogue_title(self, user_id, dialogue_id, new_title):
        # 更新對話框標題
        self.collection.update_one(
            {"_id": ObjectId(dialogue_id), "user_id": ObjectId(user_id)},
            {"$set": {"title": new_title}}
        )

    def update_dialogue_timestamp(self, dialogue_id):
        # 更新對話框最後使用時間
        self.collection.update_one(
            {"_id": ObjectId(dialogue_id)},
            {"$set": {"updated_at": datetime.now(timezone.utc)}}
        )

    def delete_dialogue(self, user_id, dialogue_id):
        # 刪除對話框
        self.collection.delete_one({"_id": ObjectId(dialogue_id), "user_id": ObjectId(user_id)})

    def get_dialogues_by_user(self, user_id):
        # 根據user_id，返回按時間排序後的對話框標題和對話框id
        dialogues = self.collection.find(
        {"user_id": ObjectId(user_id)},
        {"_id": 1, "title": 1}
        ).sort("created_at", -1)
        return [{"id": str(dialogue["_id"]), "title": dialogue["title"]} for dialogue in dialogues]

# 消息表
class Message:
    def __init__(self):
        self.collection = db['messages']

    def add_message(self, dialogue_id, user_id, message_content):
        existing_message = self.collection.find_one(
            {"dialogue_id": ObjectId(dialogue_id), "user_id": ObjectId(user_id)}
        )
        if existing_message:
            self.collection.update_one(
                {"_id": existing_message["_id"]},
                {"$push": {"messages": message_content}, "$set": {"updated_at": datetime.now(timezone.utc)}}
            )
            return str(existing_message["_id"])
        else:
            message = {
                "dialogue_id": ObjectId(dialogue_id), 
                "user_id": ObjectId(user_id),
                "messages": [message_content],
                "updated_at": datetime.now(timezone.utc) # 最後更新時間
            }
            result = self.collection.insert_one(message)
            return str(result.inserted_id)

    def get_messages_by_dialogue(self, user_id, dialogue_id):
        existing_message = self.collection.find_one(
            {"user_id": ObjectId(user_id), "dialogue_id": ObjectId(dialogue_id)},
            {"_id": 0, "messages": 1}
        )
        return existing_message.get('messages', []) if existing_message else []

    def delete_messages_by_dialogue(self, user_id, dialogue_id):
        self.collection.delete_many({"user_id": ObjectId(user_id), "dialogue_id": ObjectId(dialogue_id)})

# 所有消息表
class History:
    def __init__(self):
        self.collection = db['history']

    def add_history(self, dialogue_id, user_id, dialogue_title, message_id, content):
        existing_history = self.collection.find_one(
            {"dialogue_id": ObjectId(dialogue_id), "user_id": ObjectId(user_id), "message_id": ObjectId(message_id)}
        )
        if existing_history:
            self.collection.update_one(
                {"_id": existing_history["_id"]},
                {"$push": {"messages": content}, "$set": {"saved_at": datetime.now(timezone.utc)}}
            )
            return str(existing_history["_id"])
        else:
            history_record = {
                "dialogue_id": ObjectId(dialogue_id),
                "user_id": ObjectId(user_id),
                "dialogue_title": dialogue_title,
                "message_id": ObjectId(message_id),
                "messages": [content],
                "timestamp": datetime.now(timezone.utc), # 初次創建時間
                "saved_at": datetime.now(timezone.utc) # 最後更新時間
            }
            result = self.collection.insert_one(history_record)
            return str(result.inserted_id)

    def get_history_by_user(self, user_id):
        return list(self.collection.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1))

# 初始化对话框和消息表的对象
dialogue = Dialogue()
message = Message()
history = History()

# 添加新消息的逻辑
def save_message(user_id, dialogue_id, message_content):
    if dialogue_id:
        # 在已有对话框上新增消息
        message_id = message.add_message(dialogue_id, user_id, message_content)
        dialogue.update_dialogue_timestamp(dialogue_id)
    else:
        # 新建对话框并新增消息
        dialogue_title = dialogue.generate_title(message_content)
        dialogue_id = dialogue.create_dialogue(user_id, dialogue_title)
        message_id = message.add_message(dialogue_id, user_id, message_content)
    # 新增历史记录
    # history.add_history(dialogue_id, user_id, dialogue_title, message_id, message_content)
    return dialogue_id

# 獲取所有對話框
def get_user_dialogues(user_id):
    return dialogue.get_dialogues_by_user(user_id)

# 切換對話框的時候，根據user_id和對話框id，返回對話框相應的聊天內容和對話框id
def get_dialogue_messages(user_id, dialogue_id):
    return message.get_messages_by_dialogue(user_id, dialogue_id)


# 根據user_id和對話框id，刪除對話框表中的對話框和刪除消息表中對話框框相應的聊天內容
def delete_dialogue_and_messages(user_id, dialogue_id):
    dialogue.delete_dialogue(user_id, dialogue_id)
    message.delete_messages_by_dialogue(user_id, dialogue_id)
    return True

# 根據user_id和對話框id，更新對話框名稱
def update_dialogue_title(user_id, dialogue_id, new_title):
    dialogue.update_dialogue_title(user_id, dialogue_id, new_title)
    return dialogue_id