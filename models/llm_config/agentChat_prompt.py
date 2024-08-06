def initialize_prompt(chat_history, user_message, uploaded_files, uploaded_images, prompt_language="ZH"):
    if prompt_language == "ZH":
        prompt = f"""
請考慮以下信息以高效且有效地回應用戶的查詢。請考慮聊天記錄、用戶當前的話語以及任何上傳的文件或圖片。如果用戶的查詢與任何上傳的文件或圖片的內容相關，請分析並提供必要的信息，調用相應的工具。但是，如果用戶的查詢不需要上傳的文件或圖片，請優先直接回答他們的問題或使用其他相關工具。

### 聊天記錄
{chat_history}

### 用戶當前說的話
{user_message}

### 用戶上傳的檔案
{uploaded_files}

### 用戶上傳的圖片
{uploaded_images}

始終優先考慮用戶的當前查詢，只有在直接與用戶問題相關時才利用聊天記錄、文件或圖片。確保回應清晰、準確並有效滿足用戶需求。
                """
    else:  # Default to English
        prompt = f"""
please consider the following information to respond to the user's query efficiently and effectively. Take into account the chat history, the user's current message, and any uploaded files or images. If the user's query relates to the content of any uploaded files or images, analyze and provide the necessary information by invoking the appropriate tools. However, if the user's query does not require the uploaded files or images, prioritize answering their question directly or use other relevant tools.

### Chat History
{chat_history}

### User's Current Message
{user_message}

### Uploaded Files
{uploaded_files}

### Uploaded Images
{uploaded_images}

Always prioritize the user's current query and only utilize the chat history, files, or images if directly relevant to the user's question. Ensure the response is clear, accurate, and meets the user's needs effectively.
                """
    return prompt