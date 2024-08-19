import cohere
import requests
import os

def jinaai_rerank(query, documents, top_n, api_key=None):
    """
    https://jina.ai/reranker/
    
    """

    url = 'https://api.jina.ai/v1/rerank'

    if api_key is None:
        api_key = os.getenv('JinaAI_api_key')

    payload = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "top_n": top_n,
        "documents": documents
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(url, json=payload, headers=headers).json()
    # print(response)

    # 提取得分最高的索引
    ranked_indices = [result["index"] for result in response["results"]]
    
    return ranked_indices

def cohere_rerank(query, documents, top_n, api_key=None):
    """
    https://docs.cohere.com/reference/rerank
    
    """
    if api_key is None:
        api_key = os.getenv('JinaAI_api_key')

    co = cohere.Client(api_key)
    response = co.rerank(
    model="rerank-multilingual-v3.0",
    query=query,
    documents=documents,
    top_n=top_n,
    )
    # print(response)
    # response.results: results=[RerankResponseResultsItem(document=None, index=1, relevance_score=0.23686911), ]
    ranked_indices = [result.index for result in response.results]

    return ranked_indices


if __name__ == '__main__':
    query = "今天的天氣真不錯"
    top_n = 3
    documents = ["我後天要去健身房", "明天的天氣會好很多", "我們去購物中心吃飯羅", "我本身就是一門生意", "我不是生意人"]
    
    jinaAI_ranked_indices = jinaai_rerank(query, top_n, documents,)
    jinaAI_ranked_documents = [documents[i] for i in jinaAI_ranked_indices]
    
    cohere_ranked_indices = cohere_rerank(query, top_n, documents,)
    cohere_ranked_documents = [documents[i] for i in jinaAI_ranked_indices]

    # 排名靠前對應的索引值
    print(jinaAI_ranked_indices)
    print(cohere_ranked_indices)

    # 根據索引提取相應的文檔內容
    print(jinaAI_ranked_documents)
    print(cohere_ranked_documents)


