from langchain.vectorstores import FAISS

def create_vector_store(chunks, embedding_model):
    return FAISS.from_texts(chunks, embedding_model)
