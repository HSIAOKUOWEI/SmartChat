from ...database.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId
import gridfs


def save_to_temp_file(content, suffix):
    import tempfile
    """
        將位元組內容儲存到臨時檔案並返回檔案路徑
        :param content: 檔案的位元組內容
        :param suffix: 檔案的後綴（例如 '.pdf' 或 '.xlsx'）
        :return: 臨時檔案的路徑
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def get_source_file(file_ids):
    """
        從GridFS取得文件原始檔案
        :param file_ids: 逗號分隔的檔案ID列表
        :return: 字典，包含檔案ID、檔案名丶類型、內容(臨時檔案的路徑)
    """
    # 設置mongodb連接
    db = get_mongodb_db()
    user_file_collection = db["user_file"]
    fs = gridfs.GridFS(db)
    
    # 根據file_ids得到的gridfs_id獲取原始檔案
    source_files = {}
    
    # 将file_ids字符串分割为列表
    file_id_list = file_ids.split(',')

    for file_id in file_id_list:
        # 通過文件id以獲取gridfs_id、文件名和文件類型
        file_record = user_file_collection.find_one({"_id": ObjectId(file_id.strip())})
        if file_record:
            gridfs_id = file_record.get("gridfs_id")
            file_name = file_record.get("file_name")  
            file_type = file_record.get("file_type")
            suffix = '.' + file_name.split('.')[-1]  # 获取文件的后缀

            if gridfs_id:
                # 从GridFS中獲取文件内容
                source_file = fs.get(ObjectId(gridfs_id)).read()

                # 将文件内容保存到临时文件，并获取文件路径
                temp_file_path = save_to_temp_file(source_file, suffix)
                
                
                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": file_type,
                    "temp_file_path": temp_file_path  # 暫存檔案路徑
                }
            else:
                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": None,
                    "temp_file_path": None
                }
        else:
            source_files[file_id] = {
                "file_name": None,
                "file_type": None,
                "temp_file_path": None
            }
    
    return source_files