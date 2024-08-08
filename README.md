## SmartChat是什麼
SmartChat是一款基於Agent思想構建的開源智能聊天機器人。SmartChat可以在對話中自動調用各種工具，包括：查詢台灣天氣，網頁問答，圖片問答，圖片生成，檔案問答，搜索引擎問答，查找Arxiv論文，維基百科。

## 目錄

- [技術棧](#技術棧)
- [功能簡介](#功能簡介)
- [功能展示](#功能展示)
- [部署](#部署)
  - [本地部署](#本地部署)
  - [Docker部署](#Docker部署)
- [MongoDB表的設計](#MongoDB表的設計)
  - [Users表](#Users表)
  - [Dialogues表](#Dialogues表)
  - [Messages表](#Messages表)
  - [History表](#History表)
- [目錄結構](#目錄結構)

## 技術棧

項目使用的主要技術如下：
- 前端：HTML、JavaScript、TailwindCSS
- 後端：Flask
- 數據庫：MongoDB
- 緩存：Redis
- LLM開發框架：Langchain
- 向量數據庫：Chroma

## 功能簡介

SmartChat對話中支持的服務如下:
- 台灣天氣查詢
- 檔案問答
- 檔案總結
- 圖片對話
- 生成圖片
- 網頁問答
- 搜索引擎對話
- Arxiv論文對話
- 維基百科對話

UI基礎功能:
- 切換LLM模型
- 帳號登錄丶註冊丶重置密碼丶登出
- 聊天話框管理(新增丶刪除丶改名丶切換)
- 文件及圖片上傳


## 功能展示
 待錄影


## 部署

克隆本項目：
    ```bash
    git clone https://github.com/HSIAOKUOWEI/LLM_Ageng_flask.git
    cd LLM_Ageng_flask
    ```

### 本地部署
1. 創建並激活虛擬環境：
    ```bash
    conda create -n SmartChat python=3.10
    conda activate SmartChat

2. 安裝依賴：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置環境變量：
    ```bash
    mv .env.example .env
    ```

4. 運行項目：
    ```bash
    python app.py
    ```

### Docker部署

1. 配置環境變量：
    ```bash
    mv .env.example .env
    ```

2. 構建Docker鏡像：
    ```bash
    docker build
    ```

3. 運行Docker容器：
    ```bash
    docker-compose up
    ```

## MongoDB表的設計

### 用戶表(users)

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | MongoDB自動生成的唯一標識符 |
| account     | String    | 用戶賬號                   |
| password    | String    | 用戶密碼                   |
| last_login  | ISODate   | 用戶最後登錄時間           |
| password_last_modified  | ISODate   | 密碼更改時間    |


### 對話框表(dialogues)

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 對話框的唯一標識符         |
| user_id     | ObjectId  | 用戶標識符                  |
| title       | String    | 對話框標題                  |
| created_at  | ISODate   | 對話框的創建時間           |
| updated_at  | ISODate   | 對話框的最後更新時間       |

### 消息表(messages)

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 消息的唯一標識符           |
| user_id     | ObjectId  | 用戶標識符                  |
| dialogue_id | ObjectId  | 對話框的標識符              |  
| messages    | Array     | 消息內容的數組             |
| updated_at  | ISODate   | 消息的最後更新時間         |

### 儲存文件表(user_file)
| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 消息的唯一標識符           |
| user_id     | ObjectId  | 用戶標識符                  |
| file_name    | Array     | 文件名                     |
| file_type   | Array     | 文件類型(例如 application/pdf)|
| file_size   | Array     | 文件大小，以字節為單位      |
| gridfs_id    | Array     | 關聯到 GridFS 中存儲的文件的唯一標識符 |
| created_at   | ISODate   | 文件上傳時間             |

### 儲存圖片表(user_image)
| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 消息的唯一標識符            |
| user_id     | ObjectId  | 用戶標識符                  |
| image_name    | Array     | 圖片名稱                  |
| image_type   | Array     | 圖片類型(例如 image/png)   |
| image_size   | Array     | 圖片大小                   |
| gridfs_id    | Array     | 關聯到 GridFS 中存儲的圖片的唯一標識符 |
| created_at   | ISODate   | 圖片上傳時間             |

## 目錄結構
```plaintext
llm_flask/
├── controllers/           # 控制器層(api)
├── models/                # 模型層(處理邏輯)
│   ├── llm_config/        # LLM配置
│   ├── tools_factory/     # 服務工具類
│   ├── until/             # 數據庫及加密相關配置
│   ├── config.py          # 後端配置文件
├── static/                # 靜態文件
├── templates/             # 模板文件(展示資料)
├── .env.example           # API KEY環境變量配置
├── .gitignore             # Git 忽略文件
├── app.py                 # 應用主文件
├── docker-compose.yml     # Docker Compose 配置文件
├── Dockerfile             # Docker 構建文件
├── LICENSE                # 授權文件
├── README.md              # 項目說明文件
└── requirements.txt       # Python 依賴包