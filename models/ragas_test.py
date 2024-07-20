# data
from datasets import load_dataset

amnesty_qa = load_dataset("explodinggradients/amnesty_qa", "english_v2",trust_remote_code=True)
from ragas.metrics import (
    context_precision,
    answer_relevancy,
    faithfulness,
    context_recall,
    answer_similarity,
    answer_correctness,
)
from ragas.metrics.critique import harmfulness

# list of metrics we're going to use
metrics = [
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    harmfulness,
    answer_similarity,
    answer_correctness,
]


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from llm_flask.models.envLoad import google_api_key

google_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=google_api_key
)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

from ragas import evaluate

result = evaluate(
    amnesty_qa["eval"].select(range(1)),  # using 1 as example due to quota constrains
    metrics=metrics,
    llm=google_llm,
    embeddings=embeddings,
    is_async=False,
    raise_exceptions=False
)

print(result)