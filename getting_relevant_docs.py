import os
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Step 1: Load the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    encode_kwargs={'normalize_embeddings': True}
)


# Step 2: Load and convert JSON documents into Langchain Documents
def load_json_documents_from_folder(folder_path):
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                json_list = json.load(f)
                for item in json_list:
                    content_text = ""
                    for block in item.get("content", []):
                        if block["type"] == "paragraph":
                            content_text += block["text"] + "\n"
                        elif block["type"] == "list":
                            content_text += "\n".join(block["items"]) + "\n"

                    metadata = {
                        "header": item.get("header"),
                        "level": item.get("level"),
                        "url": item.get("url"),
                        "raw": json.dumps(item, ensure_ascii=False)  # full item retained
                    }

                    doc = Document(page_content=content_text.strip(), metadata=metadata)
                    all_docs.append(doc)
    return all_docs


# Step 3: Load documents and build FAISS index
docs = load_json_documents_from_folder("scraped_pages_final")
db = FAISS.from_documents(docs, embedding_model)
db.save_local("faiss_index_e5")


# Step 4: Search function
def search_documents(query: str, k=3):
    db = FAISS.load_local("faiss_index_e5", embedding_model, allow_dangerous_deserialization=True)
    query = f"query: {query}"  # E5 models require prefix for best performance
    results = db.similarity_search(query, k=k)

    for i, doc in enumerate(results):
        print(f"\nResult {i + 1}:")
        print("Header:", doc.metadata.get("header"))
        print("URL:", doc.metadata.get("url"))
        print("Matched Content:\n", doc.page_content)
        print("Original JSON:", doc.metadata.get("raw"))


# Example Query
search_documents("Create Application user for VRS in CUCM")