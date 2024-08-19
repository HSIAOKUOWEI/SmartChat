import os
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

def get_milvus_db(connection_args: dict = None, collection_name: str = None, embeddings=None, docs=None):
    """
    初始化並返回一個 Milvus 實例。

    參數:
        connection_args (dict, 可選): 包含 Milvus 伺服器連接參數的字典，包括 'host' 和 'port'。如果未提供，將從環境變量中獲取默認值。
        collection_name (str, 可選): 要連接的 Milvus 集合名稱。如果未提供，將從環境變量中獲取默認值。
        embeddings (可選): 自定義的嵌入實例。如果未提供，將使用 OpenAI 的 API 密鑰創建一個 OpenAIEmbeddings 實例。
        docs (可選): 要插入 Milvus 集合中的文檔。如果提供，將使用這些文檔初始化集合。

    返回:
        Milvus: 已初始化的 Milvus 實例。
    """

    # 設置預設集合名稱
    if collection_name is None:
        collection_name = os.getenv("MILVUS_COLLECTION_NAME", "example_collection")
    
    # 設置預設連接參數
    if connection_args is None:
        connection_args = {
            "host": os.getenv("MILVUS_IP", "127.0.0.1"),
            "port": int(os.getenv("MILVUS_PORT", 19530))
        }
    
    # 設置預設嵌入實例
    if embeddings is None:
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    # 初始化 Milvus 實例
    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name=collection_name,
        collection_description="example description"  # 可選的集合描述
    )
    
    # 如果提供了文檔，將其插入到集合中
    if docs:
        vector_store = vector_store.from_documents(
            documents=docs, 
            embedding_field=embeddings,
            collection_name=collection_name,
            connection_args=connection_args
        )
        

    return vector_store
# 示例使用
if __name__ == "__main__":
    vector_store = get_milvus_db()
    print("Milvus vector store initialized:", vector_store)