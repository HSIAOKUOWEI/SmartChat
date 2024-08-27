from ...database.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId
import gridfs
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers.pdf import PyPDFParser


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

            if gridfs_id:
                # 从GridFS中獲取文件内容
                source_file = fs.get(ObjectId(gridfs_id)).read()
                documents_stream = Blob.from_data(source_file)

                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": file_type,
                    "documents_stream": documents_stream  # 暫存檔案路徑
                }
            else:
                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": None,
                    "documents_stream": None
                }
        else:
            source_files[file_id] = {
                "file_name": None,
                "file_type": None,
                "documents_stream": None
            }
    
    return source_files