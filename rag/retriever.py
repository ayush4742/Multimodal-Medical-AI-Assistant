import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_FAISS_PATH = "rag/faiss_index"


class MedicalRetriever:

    def __init__(self):

        print("Loading Embedding Model...")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Loading FAISS Index...")

        self.db = FAISS.load_local(
            DB_FAISS_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        print("Retriever Ready!")

    def retrieve(self, query, k=4):

        docs = self.db.similarity_search(
            query,
            k=k
        )

        context = ""

        for i, doc in enumerate(docs, start=1):

            context += f"\n\n========== Medical Context {i} ==========\n"

            context += doc.page_content

        return context


retriever = MedicalRetriever()


def retrieve_medical_context(query):
    return retriever.retrieve(query)


# Testing
if __name__ == "__main__":

    query = "I have itchy red skin with rashes."

    context = retrieve_medical_context(query)

    print(context)