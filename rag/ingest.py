import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Folder containing PDFs
DATA_PATH = "knowledge_base"

# Folder where FAISS index will be stored
DB_FAISS_PATH = "rag/faiss_index"


def create_vector_db():

    print("=" * 60)
    print("Loading PDFs...")
    print("=" * 60)

    loader = PyPDFDirectoryLoader(DATA_PATH)

    documents = loader.load()

    print(f"Total Pages Loaded : {len(documents)}")

    print("=" * 60)
    print("Splitting Documents...")
    print("=" * 60)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(documents)

    print(f"Total Chunks : {len(texts)}")

    print("=" * 60)
    print("Loading Embedding Model...")
    print("=" * 60)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("=" * 60)
    print("Creating FAISS Index...")
    print("=" * 60)

    db = FAISS.from_documents(
        texts,
        embedding_model
    )

    os.makedirs(DB_FAISS_PATH, exist_ok=True)

    db.save_local(DB_FAISS_PATH)

    print("=" * 60)
    print("FAISS Index Created Successfully")
    print(f"Saved at : {DB_FAISS_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    create_vector_db()