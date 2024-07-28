from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def load_vector_stores(internal_path, external_path, grievances_path, embeddings_model):
    external_policy_db = FAISS.load_local(external_path, embeddings_model, allow_dangerous_deserialization=True)
    internal_policy_db = FAISS.load_local(internal_path, embeddings_model, allow_dangerous_deserialization=True)
    grievances_db = FAISS.load_local(grievances_path, embeddings_model, allow_dangerous_deserialization=True)
    return external_policy_db, internal_policy_db, grievances_db
