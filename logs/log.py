import logging
import os

# 建立日誌記錄器
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG) # 設定日誌等級為 DEBUG

# 從環境變數中取得日誌檔案路徑 
log_file_path = os.getenv('LOG_FILE_PATH', 'app.log') # 預設記錄檔名稱為 app.log

# 建立一個檔案處理器，將日誌輸出到檔案 
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG) # 檔案處理器的日誌等級設定為 DEBUG

# 建立一個控制台處理器，將日誌輸出到控制台 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG) # 控制台處理器的日誌等級設定為 DEBUG 

# 建立格式化器，定義日誌輸出的格式 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter) # 將格式化器新增至檔案處理器 
console_handler.setFormatter(formatter) # 將格式化器新增至控制台處理器 

# 將處理器加入記錄器 
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 父子日志通過前綴來表示：app_logger.son_logger，app_logger——父級，son_logger——子級
# True：代碼子級的日誌會傳遞到父級日誌中
# False：代碼子級日誌只保存在自己日誌中，不會傳遞到父級日誌中
logger.propagate = False