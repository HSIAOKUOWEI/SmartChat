## 項目簡介

這是一個XXXX項目，旨在解決XXXX問題。該項目使用XXXX技術棧來實現功能，主要包含XXXX功能模塊。

## 目錄

- [功能簡介](#功能簡介)
- [功能展示](#功能展示)
- [技術棧](#技術棧)
- [功能模塊](#功能模塊)
- [部署](#部署)
  - [本地部署](#本地部署)
  - [Docker部署](#Docker部署)
- [MongoDB表的設計](#MongoDB表的設計)
  - [Users表](#Users表)
  - [Dialogues表](#Dialogues表)
  - [Messages表](#Messages表)
  - [History表](#History表)
- [目錄結構](#目錄結構)

## 功能簡介

基礎功能:
- 用戶註冊和登錄
- 會話管理
- 文件上傳和處理
- 聊天歷史記錄
對話功能


## 功能展示

展示項目功能的截圖或GIF，並簡要說明每個展示的功能。

## 技術棧

列出項目使用的主要技術，包括但不限於：
- 前端：HTML、JavaScript、TailwindCSS
- 後端：Flask
- 數據庫：MongoDB、
- 緩存：Redis

## 功能模塊

詳細描述項目的各個功能模塊及其作用，例如：
- 用戶管理模塊
- 對話框管理模塊
- 消息管理模塊
- 歷史記錄管理模塊

## 部署

### 本地部署

1. 克隆本項目：
    ```bash
    https://github.com/HSIAOKUOWEI/LLM_Ageng_flask.git
    cd LLM_Ageng_flask
    ```

2. 安裝依賴：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置環境變量：
    ```bash
    .env
    ```

4. 運行項目：
    ```bash
    python app.py
    ```

### Docker部署

1. 構建Docker鏡像：
    ```bash
    docker build
    ```

2. 運行Docker容器：
    ```bash
    docker-compose up
    ```

## MongoDB表的設計

### Users表

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | MongoDB自動生成的唯一標識符 |
| account     | String    | 用戶賬號                   |
| password    | String    | 用戶密碼                   |
| created_at  | ISODate   | 用戶註冊時間               |
| last_login  | ISODate   | 用戶最後登錄時間           |

### Dialogues表

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 對話框的唯一標識符         |
| user_id     | ObjectId  | 創建對話框的用戶標識符     |
| title       | String    | 對話框的標題               |
| created_at  | ISODate   | 對話框的創建時間           |
| updated_at  | ISODate   | 對話框的最後更新時間       |

### Messages表

| 字段名      | 類型      | 描述                       |
|-------------|-----------|----------------------------|
| _id         | ObjectId  | 消息的唯一標識符           |
| dialogue_id | ObjectId  | 關聯到對話框的標識符       |
| user_id     | ObjectId  | 發送消息的用戶標識符       |
| messages    | Array     | 消息內容的數組             |
| timestamp   | ISODate   | 消息的創建時間             |
| updated_at  | ISODate   | 消息的最後更新時間         |

### History表

| 字段名        | 類型      | 描述                       |
|---------------|-----------|----------------------------|
| _id           | ObjectId  | 歷史記錄的唯一標識符       |
| dialogue_id   | ObjectId  | 關聯到對話框的標識符       |
| user_id       | ObjectId  | 參與聊天的用戶標識符       |
| dialogue_title| String    | 對話框的標題               |
| message_id    | ObjectId  | 關聯到消息的唯一標識符     |
| content       | Array     | 消息歷史記錄               |
| timestamp     | ISODate   | 消息的歷史記錄時間         |
| saved_at      | ISODate   | 歷史記錄保存的時間         |

## 目錄結構