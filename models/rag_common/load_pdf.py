# https://api.python.langchain.com/en/latest/vectorstores/langchain_astradb.vectorstores.AstraDBVectorStore.html
import fitz


def pdf_to_images(pdf_path, output_folder):
    # 打開PDF文檔
    pdf_document = fitz.open(pdf_path)
    
    # 遍歷每一頁
    for page_number in range(len(pdf_document)):
        # 獲取頁面
        page = pdf_document.load_page(page_number)
        
        # 將頁面渲染為像素圖像
        pix = page.get_pixmap()
        
        # 保存圖像
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        pix.save(output_path)
        print(f"Page {page_number + 1} saved as {output_path}")

    # 關閉PDF文檔
    pdf_document.close()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_pdf_documents(file_path: str) -> list[Document]:
    loader = PyPDFLoader(file_path=file_path, extraction_mode="plain")
    return loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter())



if __name__ == "__main__":
    print(load_pdf_documents("test.pdf"))
