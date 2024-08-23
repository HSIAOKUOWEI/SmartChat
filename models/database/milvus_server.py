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
        collection_name = os.getenv("MILVUS_COLLECTION_NAME", "langchain")
    
    # 設置預設連接參數
    if connection_args is None:
        connection_args = {
            "host": os.getenv("MILVUS_IP", "127.0.0.1"),
            "port": int(os.getenv("MILVUS_PORT", 19530))
        }
    # 設置預設嵌入實例
    if embeddings is None:
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        
    # dim = len(embeddings.embed_query("1")) # 自動獲取向量維度
    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name=collection_name,
        collection_description="example description",
        vector_field="vector",  # 这是存储向量的字段名称
        collection_properties={"vector": {"dim": 1536}},  # 设置向量字段的维度
        auto_id=True,
        drop_old=True
    )

    # 如果提供了文檔，將其插入到集合中
    if docs:
        try:
            vector_store.add_documents(documents=docs, auto_id=True)
        except Exception as e:
            print(f"Error inserting documents: {e}")
            return None

    return vector_store
        
# 示例使用
if __name__ == "__main__":
    from langchain_core.documents import Document
    docs = [Document(page_content="asdasdasd", metadata={"user_id": "66ba11111892ec02d977971a"}), 
            Document(page_content="asdasdasd", metadata={"user_id": "66ba11111892ec02d977971a"}), 
            Document(page_content="sadasd", metadata={"user_id": "66ba11111892ec02d977971a"})]
    
    
    vector_store = get_milvus_db(docs=docs)
    print("Milvus vector store initialized:", vector_store)