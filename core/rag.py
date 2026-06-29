from rag.retriever import retrieve_medical_context


def retrieve(query: str) -> str:
    """
    Wrapper around Medical FAISS Retriever.
    Always returns a string.
    """

    if not query:
        return ""

    try:

        context = retrieve_medical_context(query)

        if context is None:
            return ""

        return context

    except Exception as e:

        print(f"[RAG ERROR] {e}")

        return ""


def retrieve_with_history(
    patient_query: str,
    conversation_history: str
) -> str:
    """
    Retrieves context using both conversation
    history and current patient query.
    """

    search_query = f"""
Conversation:
{conversation_history}

Current Complaint:
{patient_query}
"""

    return retrieve(search_query)


def health_check():

    try:

        retrieve("Headache")

        return True

    except Exception:

        return False


if __name__ == "__main__":

    print(retrieve("I have chest pain"))