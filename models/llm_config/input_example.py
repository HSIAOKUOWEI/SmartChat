from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from llm_flask.models.envLoad import google_api_key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",google_api_key=google_api_key)

message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "What's in this image?",
        },  # You can optionally provide text parts
        {"type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"},
    ]
)
llm.invoke([message])